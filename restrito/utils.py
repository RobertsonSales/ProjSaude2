import mysql.connector
import hashlib
import smtplib
import random
import string
import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Função de conexão com o banco de dados
def create_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="****",
        password="****",
        database="projsaude"
    )
    return conn

# Função de hash de senha
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Função de autenticação
def authenticate_user(email, password):
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT username, password, email FROM usuarios WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    #print (result)
    conn.close()

    if result and result[1] == hash_password(password):
        return True
    return False

# Função para enviar e-mail com o token de recuperação de senha
def send_recovery_email(user_email, recovery_token):
    # Configurações do servidor de e-mail
    sender_email = "projetosaude@gmail.com"  # Troque pelo seu e-mail
    sender_password = "****"         # Troque pela sua senha de e-mail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Configuração do e-mail
    message = MIMEMultipart()
    message["De: "] = sender_email
    message["Para: "] = user_email
    message["Assunto: "] = "Recuperação de Senha"

    # Corpo do e-mail
    body = f"""
    Você solicitou a redefinição de senha.
    Use o código abaixo para redefinir sua senha:

    Código de recuperação: {recovery_token}

    Se você não solicitou a redefinição de senha, ignore este e-mail.
    """
    message.attach(MIMEText(body, "plain"))

    try:
        # Enviar o e-mail
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
        server.quit()
        return True
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")
        return False

# Função para gerar um token de recuperação
def generate_recovery_token():
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(8))
    return token

# Função para salvar o token de recuperação no banco de dados
def save_recovery_token(email, token):
    conn = create_connection()
    cursor = conn.cursor()
    query = "UPDATE usuarios SET recovery_token = %s WHERE email = %s"
    cursor.execute(query, (token, email))
    conn.commit()
    conn.close()

# Função de recuperação de senha
def recover_password(email):
    conn = create_connection()
    cursor = conn.cursor()

    # Verificar se o e-mail existe no banco de dados
    query = "SELECT email FROM usuarios WHERE email = %s"
    cursor.execute(query, ([email]))
    result = cursor.fetchone()

    if result:
        # Gerar o token de recuperação
        recovery_token = generate_recovery_token()
        
        # Salvar o token no banco de dados
        save_recovery_token(email, recovery_token)
        
        # Enviar o e-mail com o token
        if send_recovery_email(email, recovery_token):
            st.success(f"Um e-mail com o código de recuperação foi enviado para {email}.")
        else:
            st.error("Erro ao enviar o e-mail de recuperação.")
    else:
        st.error("Este e-mail não está registrado.")

    conn.close()

# Função para redefinir a senha
def reset_password(email, recovery_token, new_password):
    conn = create_connection()
    cursor = conn.cursor()

    # Verificar se o token de recuperação está correto
    query = "SELECT recovery_token FROM usuarios WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()

    if result and result[0] == recovery_token:
        # Atualizar a senha do usuário
        hashed_password = hash_password(new_password)
        query = "UPDATE usuarios SET password = %s, recovery_token = NULL WHERE email = %s"
        cursor.execute(query, (hashed_password, email))
        conn.commit()
        st.success("Sua senha foi alterada com sucesso.")
    else:
        st.error("Token de recuperação inválido.")

    conn.close()

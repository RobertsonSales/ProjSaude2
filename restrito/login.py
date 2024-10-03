import streamlit as st
from restrito.utils import authenticate_user, hash_password, recover_password, reset_password, create_connection

def login_page():

    # Verifica se o usuário está logado ou não no st.session_state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    menu = ["Login", "Registrar-se", "Esqueci minha senha"]
    choice = st.selectbox("Selecione uma forma de acesso:", menu)

    if choice == "Login":
        st.subheader("Fazer Login")

        nome = st.text_input("Usuário")
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")

        if st.button("Login"):
            if authenticate_user(email, password):
                st.success('Usuário =>  '+nome+'  Logado com sucesso!')
                st.session_state.logged_in = True  # Definindo como logado
                #st.session_state(logged_in="true")  # Simula um redirecionamento por query params
            else:
                st.error("E-mail ou senha incorretos.")

    elif choice == "Registrar-se":
        st.subheader("Registrar-se")

        nome = st.text_input("Novo Usuário")
        new_email = st.text_input("Novo Email")
        new_password = st.text_input("Nova Senha", type="password")
        token = 0

        if st.button("Registrar"):
            conn = create_connection()
            cursor = conn.cursor()

            # Verifica se o email já está registrado
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (new_email,))
            result = cursor.fetchone()

            if result:
                st.warning("Este e-mail já está registrado!")
            else:
                # Inserir novo usuário
                hashed_password = hash_password(new_password)                
                cursor.execute("INSERT INTO usuarios (username, email, password, recovery_token) VALUES (%s, %s, %s, %s)", (nome, new_email, hashed_password, token))
                conn.commit()
                st.success("Usuário registrado com sucesso!")

            conn.close()

    elif choice == "Esqueci minha senha":
        st.subheader("Recuperar Senha")

        email = st.text_input("Digite seu e-mail")

        if st.button("Recuperar senha"):
            recover_password(email)  # Função para enviar o token de recuperação de senha

        st.subheader("Redefinir Senha")
        recovery_token = st.text_input("Digite o código de recuperação recebido")
        new_password = st.text_input("Digite sua nova senha", type="password")

        if st.button("Redefinir senha"):
            reset_password(email, recovery_token, new_password)  # Função para redefinir a senha


def logout():
    """Função para logout"""
    st.session_state.logged_in = False
    #st.query_params(logged_in="false")
    st.success("Você saiu com sucesso.")

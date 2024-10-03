import mysql.connector
import streamlit as st  

def create_connection():
    # Usando st.secrets para acessar as variáveis do secrets.toml
    con = mysql.connector.connect(
        host=st.secrets["mysql"]["DB_HOST"],
        user=st.secrets["mysql"]["DB_USER"],
        password=st.secrets["mysql"]["DB_PASSWORD"],
        database=st.secrets["mysql"]["DB_NAME"]
    )
    cursor = con.cursor()  # Criando o cursor
    return con, cursor  # Retornando a conexão e o cursor

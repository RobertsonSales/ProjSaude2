import streamlit as st
from streamlit_option_menu import option_menu
import restrito.login as login
import restrito.crud_grupo as crud_grupo
import restrito.crud_unidade as crud_unidade
import restrito.crud_setor as crud_setor

def check_login():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("Faça login no menu lateral para acessar esta página.")
        st.stop()
    
def Limp():
    st.empty()
    a=0
    b = 30
    while a <b:
        st.write('                ')
        a=a+1

def private():

    with st.container(border=True):

        page = ('-',"Login", "Gerenciar Grupos", "Gerenciar Unidades", "Gerenciar Setores")
        page = st.selectbox("GRUPOS DE UNIDADES DE SAÚDE:", page)

        st.session_state['current_page'] = page

        if st.session_state['current_page'] == "Login":
            login.login_page()
            #Limp()
        elif st.session_state['current_page'] == "Gerenciar Grupos":
            check_login()
            crud_grupo.show_grupos_crud()
            Limp()
        elif st.session_state['current_page'] == "Gerenciar Unidades":
            check_login()
            crud_unidade.show_unidades_crud()
            Limp()
        elif st.session_state['current_page'] == "Gerenciar Setores":
            check_login()
            crud_setor.show_setores_crud()
            Limp()




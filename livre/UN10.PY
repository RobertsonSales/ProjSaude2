import streamlit as st 
import Querys
from Cadastro import Incluir, alt_plus, Excluir

def Int():

    st.subheader('Área restrita do sistema - Movimentação do cadastro:')

    Op = st.selectbox('Qual sua opção (Incluir, Alterar, Excluir)? ',['Nenhuma','Incluir', 'Alterar', 'Excluir'])

    if Op =='Incluir':
        Incluir.Inc()

    if Op =='Alterar':
        alt_plus.Alt()

    if Op =='Excluir':
        Excluir.Exc()
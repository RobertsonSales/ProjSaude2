import streamlit as st
import livre.UN1,livre.UN2,livre.UN3,livre.UN4,livre.UN5,livre.UN6,livre.UN7,livre.UN8,livre.UN9

def List_Unid():

    with st.container(border=True):        
        st.write('UNIDADES DE SAÚDE - RIO DE JANEIRO - ESCOLHA UM GRUPO PARA PESQUISAR')

    with st.container(border=True):
        page = ('-','UPAS - 24H', 'CER - 24H', 'HOSPITAIS ESTADUAIS','HOSPITAIS MUNICIPAIS','POLICLÍNICAS','CLÍNICAS DA FAMÍLIA','UNIDADES BÁSICAS DE SAÚDE','CENTROS DE REFERÊNCIA','CAPS')
        page = st.selectbox("GRUPOS DE UNIDADES DE SAÚDE:", page)

    if page == 'UPAS - 24H':
        livre.UN1.List()

    elif page == 'CER - 24H':
        livre.UN2.List()

    elif page == 'HOSPITAIS ESTADUAIS':
        livre.UN3.List()

    elif page == 'HOSPITAIS MUNICIPAIS':
        livre.UN4.List()

    elif page == 'POLICLÍNICAS':
        livre.UN6.List()

    elif page == 'CLÍNICAS DA FAMÍLIA':
        livre.UN5.List()

    elif page == 'UNIDADES BÁSICAS DE SAÚDE':
        livre.UN7.List()

    elif page == 'CENTROS DE REFERÊNCIA':
        livre.UN8.List()

    elif page == 'CAPS':
        livre.UN9.List()


            

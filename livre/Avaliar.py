import streamlit as st
import Querys

def Upas():

    st.subheader('Cadastro de UPAs - Avaliação de Unidades')

    with st.container(border=True):

        colun = st.columns((2,16,6,4))
        
        campos = ['Cod', 'Unidade', 'Telefone', 'Avaliar']

        for colun, campos in zip(colun, campos):

            colun.write(campos)

        for item in (Querys.Select()):

            col1, col2, col5, col6 = st.columns((2,16,6,4))

            col1.write(item[11])
            col2.write(item[0])        
            col5.write(item[8])
        
            button_space_Avaliar = col6.empty()
            on_click_Avaliar = button_space_Avaliar.button('Avaliar', 'btnAvaliar' + str(item[11]))
            
        if on_click_Avaliar: 
            
            with st.container(border=True):
                st.subheader('Avaliando: =>'+item[0], divider=True)
                op = st.selectbox('Selecione um eixo para avaliar: ', ('-','Assistencial', 'Administrativo', 'Operacional'))
                with st.form(key='Avalia', border=True):
 
                    if op == 'Assistencial':
                        a = 0
                        td = 5
                        for a in td:
                            with st.container(border=True):
                                ac = st.radio('Com relação ao Acolhimento recebido, você se considera: ', ' ','Muito satisfeito', 'Pouco satisfeito', 'Insatisfeito')
                                if ac == 'Muito satisfeito':
                                    grau = 3
                                elif ac == 'Satisfeito':
                                    grau = 2
                                elif ac == 'Satisfeito':
                                    grau = 1
                                a +=1  
                                with st.container(border=True):
                                    Av = st.radio('Com relação a demora para ter seu risco avaliado, você considera: ', ' ','Muito rápido', 'Demorado', 'Muito demorado')
                                    if Av == 'Muito rápido':
                                        grau = 3
                                    elif Av == 'Demorado':
                                        grau = 2
                                    elif Av == 'Muito demorado':
                                        grau = 1
                                    a +=1  
                                    with st.container(border=True):
                                        Cs = st.radio('Com relação a demora para seer consultado pelo médico, você considera: ', ' ','Muito rápido', 'Demorado', 'Muito demorado')
                                        if Cs == 'Muito rápido':
                                            grau = 3
                                        elif Cs == 'Demorado':
                                            grau = 2
                                        elif Cs == 'Muito demorado':
                                            grau = 1
                                        a +=1  
                                        with st.container(border=True):
                                            Ex = st.radio('O médico solicitou exames de imagem e/ou outros?: ', ' ','Vários exames', 'Um exame', 'Nenhum exame')
                                            if Ex == 'Vários exames':
                                                grau = 3
                                            elif Ex == 'Um exame':
                                                grau = 2
                                            elif Ex == 'Nenhum exme':
                                                grau = 1
                                            a +=1  
                                            with st.container(border=True):
                                                Md = st.radio('A medicação prescrita foi aplicada/dispensada na/pela unidade?: ', ' ','Todos os medicamentos', 'Alguns medicamentos', 'Nenhum medicamento')
                                                if Md == 'Todos os medicamentos':
                                                    grau = 3
                                                elif Md == 'Alguns medicamentos':
                                                    grau = 2
                                                elif Md == 'Nenhum medicamento':
                                                    grau = 1
                                                a +=1 
                                                st.form_submit_button('Avançar')

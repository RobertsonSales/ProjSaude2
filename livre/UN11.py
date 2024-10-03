import streamlit as st

def livros():

    st.subheader('Permita-se degustar um bom livro', divider=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        cam_arq_1 = './image/Livro1.jpg'
        st.image(cam_arq_1, caption='A Ciência da Separação - Da indignação ao respeito')
        
    with col2:
        cam_arq_2 = './image/Livro2.jpg'
        st.image(cam_arq_2, caption='Liberdade de escolha - Nos domínios da Fé')

    with col3:
        cam_arq_3 = './image/Livro3.jpg'
        st.image(cam_arq_3, caption='A Ciência da União - Da ilusão à realidade')#btn3 = st.button('Ir à loja')
        
    #st.divider()

    select = st.selectbox("Selecione um livro para ler sua sinopse ou ir à loja:", ('Nenhum livro selecionado','A Ciência da Separação','Liberdade de escolha', 'A Ciência da União'))

    if select == 'A Ciência da Separação':
        with st.container(border=True):
            cam_arq_1 = './image/Livro1.jpg'
            st.image(cam_arq_1, width=300)
            st.write("A obra traz à luz a necessidade de distinguirmos conceitos amplamente divulgados, mas muitas vezes confundidos ao longo de décadas e até séculos. Os conceitos de dor e sofrimento, de liberdade, de pecado, de viver e de existir são bastante esmiuçados, além do sentimento de posse. E uma importante ferramenta de análise das relações é entregue ao leitor, na forma de três balizadores considerados pelo autor como fundamentais, que são a Afinidade, a Dependência e a Conveniência.")
            st.write('Para ir à loja, [Clique Aqui: ](https://loja.uiclap.com/titulo/ua28740/?srsltid=AfmBOoq8jPwPg7H7kVoDlQ8KInmGoP2T_jOcFvUwhoG-lB1uhQmJ4Lyz)')
        
    if select == 'Liberdade de escolha':
        with st.container(border=True):
            cam_arq_1 = './image/Livro2.jpg'
            st.image(cam_arq_1, width=300)
            st.write("O padre e missionário Hildebrandt Scott, um inglês naturalizado brasileiro, pretende construir mais uma escola ou centro educativo para jovens e adultos, e por isso busca o apoio da prefeitura local da cidade onde vem atuando como pároco. Inicialmente apoiado pela Igreja Católica, da qual é membro há várias décadas, representada aqui por um bispo que fora seu mestre e tutor desde o início de sua carreira, durante o processo ele conhece algumas figuras com as quais se vê às voltas com discussões sobre diversos fenômenos que podem vir a abalar sua fé. O estopim do processo é Rodrigo, um rapaz cuja personalidade singular lhe chama muito a atenção, o qual demonstra grande destreza em compreender diversos mecanismos religiosos, sem, no entanto, participar de nenhuma seita ou instituição religiosa. Conhece também Samuel, um líder comunitário que é membro de uma ordem iniciática para-maçônica e praticante da Umbanda, e, junto com o prefeito da cidade, que é maçom, passa a promover vários encontros onde os diálogos passeiam por diversos temas correlatos. Hildebrandt relata ainda, no curso desta obra, experiências extrassensoriais cuja relevância pode levar o leitor a viajar pelo universo do esoterismo, ainda que em pequenas doses. Raina, irmã de Rodrigo e professora primária de uma comunidade rural, responde pela pimenta no vatapá de Hildebrandt.")
            st.write('Para ir à loja, [Clique Aqui: ](https://loja.uiclap.com/titulo/ua28081/?srsltid=AfmBOopuWbGgxnafbiTSVSQjmUALOrj0SkloiFM5ItPIDkZK8TisEazm)')

    if select == 'A Ciência da União':
        with st.container(border=True):
            cam_arq_1 = './image/Livro3.jpg'
            st.image(cam_arq_1, width=300)
            st.write("Nesta obra o leitor terá a oportunidade de compreender o quanto vem atuando no mundo sem conhecimento do que possa vir a ser a verdadeira e mais importante união, aquela que devia ser buscada desde a primeira, que foi incondicional. Nossa chegada no mundo fenomênico, na condição hominal, jamais terá sido a primeira oportunidade de manifestação de nosso Espírito, essa parte de nosso Ser que é imortal. Tomar ciência dos fragmentos que nos compõem e das instâncias de nosso Ser que formam um verdadeiro complexo pode ser de grande utilidade na busca pelo autoconhecimento. Trazidos da Psicanálise, Id, Ego e Superego são associados à noção de indivíduo (corpo físico), eu (Alma) e sujeito (Espírito), numa importante analogia, que muito pode contribuir para o desenvolvimento de muitos de nós.")
            st.write('Para ir à loja, [Clique Aqui: ](https://loja.uiclap.com/titulo/ua27600/?srsltid=AfmBOoqy5Tfbc0x5kBseyMLAWr9Fdp1iYN-0H8QCTYUgaAUqfR-YaUqf)')

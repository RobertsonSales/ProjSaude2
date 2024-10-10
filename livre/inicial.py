import streamlit as st 
import webbrowser
import livre.UN11 as UN11

def motivo():

  st.subheader('Razões para esta aplicação existir:', divider=True) 

  with st.container(border=True):

    col1, col2, col3 = st.columns(3)

  with col1:
      with st.expander('Sobre o autor:'):
        cam_arq_1 = './image/Foto Sales.jpeg'
        st.image(cam_arq_1, width=190)            
        st.write("Atuei por quase 14 anos em diversos projetos da Secretaria de Estado de Governo (SEGOV) e da Secretaria de Estado da Casa Civil (SECC). Dentre os projetos em que atuei está a extinta Operação SOS Saúde (idealizado pelo então Subsecretário de Governo, Reynaldo Braga, juntamente com a Psicóloga Eliana Guerra), na qual atuei por quase 5 anos. Essa Operação realizava o monitoramento de toda a rede própria estadual, promovendo o atendimento humanizado dos cidadãos, conforme preconiza o SUS.")
        st.write('Acesse meu canal [Aqui:](https://www.youtube.com/@iscutaqui)')
          
  with col2:
      with st.expander('Sobre a Saúde'):
        cam_arq_2 = './image/Col1.jpg'
        st.image(cam_arq_2, width=190)
        st.write("A questão da Saúde, ao ser levantada, sempre gera comentários muitas vezes negativos, especialmente quando tratamos do serviço público oferecido aos cidadãos, não é mesmo? Este sistema foi criado para que você possa contribuir com sua avaliação sobre a qualidade do serviço recebido, visando à melhoria no atendimento, como um todo. No meu canal no YouTube eu dou várias dicas sobre como usufruir da melhor maneira possível desse que é o melhor sistema de saúde pública do ocidente, o SUS.")
        st.write('Acesse meu canal [Aqui:](https://www.youtube.com/@iscutaqui)')

  with col3:
      with st.expander('Sobre o SUS:'):
        cam_arq_3 = './image/SUS.jpg'
        st.image(cam_arq_3, width=190)
        st.write("O Sistema Único de Saúde é um dos maiores e mais complexos sistemas de saúde pública do mundo, abrangendo desde a simples aferição da pressão arterial, pela Atenção Primária, até o transplante de órgãos, garantindo acesso integral, universal e gratuito para toda a população do país. Com a sua criação, o SUS proporcionou o acesso universal ao sistema público de saúde, sem discriminação. A atenção integral à saúde, e não somente aos cuidados assistenciais (...).")
        st.write('Fonte: [Min.da Saúde:](https://www.gov.br/saude/pt-br/sus)')

  with st.container(border=True):

    OP = st.selectbox('Para mais experiências, selecione uma opção: ', [' -- ','Nenhuma','Vídeos sobre o SUS', 'Livros do autor'])  

    if OP == 'Nenhuma':
      st.warning('Escolha uma opção válida (com conteúdo) e depois clique em Avançar!')
    
    if OP == 'Livros do autor':
      UN11.livros()

    if OP == 'Vídeos sobre o SUS':
      
      with st.expander('Selecione o tema desejado:'):

        st.write('Princípios e diretrizes do SUS [Clique aqui](https://m.youtube.com/watch?v=YJaEz2qBveY)')
        st.write('Aprendendo com exemplos [Clique aqui](https://m.youtube.com/watch?v=dsXvFGQBKUU&t=25s)')
        st.write('Um desenho sobre o SUS [Clique aqui](https://m.youtube.com/watch?v=Av6lGVElqds)')




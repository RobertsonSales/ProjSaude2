import streamlit as st
from streamlit_option_menu import option_menu
import livre.inicial as inicial
import livre.unidades as unid
import restrito.privativo as privativo
from PIL import Image
import time

# Função para converter cm para pixels (resolução de 96 DPI)
def cm_to_px(cm):
    return int(cm * 37.7952755906)  # 1 cm = 37.79 pixels aproximadamente

# Dimensões desejadas em cm
altura_cm = 5.5
largura_cm = 8.5

def Limp():
    st.empty()
    a=0
    b = 30
    while a <b:
        st.write('                ')
        a=a+1

with st.sidebar:
    page = option_menu(
        "Faça sua opção:",
        ["Página Inicial", "Unidades de Saúde", "Avaliar Unidades", "Área restrita"],
        icons=["house", "hospital", "building", "clipboard-data"],
        default_index=0,
    )

st.subheader("Sistema para avaliação das Unidades de Saúde - RJ", divider=True)
#with st.container(border=True):
 #   cam_arq_1 = 'image/inicial2.jpg'
  #  st.image(cam_arq_1, width=670)

# Redirecionamento das páginas
# Lista de URLs ou caminhos para as imagens

if page == "Página Inicial":
    inicial.motivo()
    Limp()

elif page == "Unidades de Saúde":  
    unid.List_Unid()
    Limp()

elif page == "Área restrita":
    privativo.private()
    Limp()

elif page == "Avaliar Unidades":
    st.warning('Esta funcionalidade está em desenvolvimento e em breve estará disponível.')
    Limp()


with st.sidebar:
    imagens = [
        "image/hospital.jpg",
        "image/Upa.jpg",
        "image/ubs.jpg",
        "image/Cli_fam.jpg",
        "image/Corr1.jpg",
        "image/uti1.jpg",
        "image/ubs.jpg",
        "image/col4.jpg"

        ]
    
    # Variável para armazenar o índice atual da imagem
    if 'img_index' not in st.session_state:
        st.session_state.img_index = 0

    # Container vazio para a imagem
    image_container = st.empty()

    # Loop para exibir as imagens

    while True:        
            # Carrega e redimensiona a imagem
        img = Image.open(imagens[st.session_state.img_index])
        img = img.resize((cm_to_px(largura_cm), cm_to_px(altura_cm)))  # Redimensiona a imagem

        # Atualiza a imagem no container
        image_container.image(img)

        # Incrementa o índice da imagem
        st.session_state.img_index = (st.session_state.img_index + 1) % len(imagens)

        # Aguardar 3 segundos antes de mudar a imagem
        time.sleep(2)






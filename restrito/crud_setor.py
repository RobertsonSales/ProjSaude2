import streamlit as st
from restrito.utils import create_connection
import pandas as pd
from fpdf import FPDF
import base64
import os


def delete_setor(selected_setor_id):
    """
    Exclui o setor do banco de dados com o ID fornecido.
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM setor WHERE id_setor = %s", (selected_setor_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_setores():
    """
    Busca todos os setores do banco de dados.
    """
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_setor, nome_nome FROM setor")
    setores = cursor.fetchall()
    cursor.close()
    conn.close()
    return setores

def get_setores_by_unidade(selected_unidade_id):
    """
    Busca todos os setores vinculados à unidade informada.
    """
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_setor, nome_setor, G1, G2, G3, G4, taxa FROM setor WHERE id_unidade = %s", (selected_unidade_id,))
    setores = cursor.fetchall()
    cursor.close()
    conn.close()
    return setores

def get_all_grupos():
 
    #Busca todos os grupos do banco de dados.
 
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_grupo, nome_grupo FROM grupo")
    grupos = cursor.fetchall()
    cursor.close()
    conn.close()
    return grupos

def calculate_column_widths(dataframe, pdf, padding=5):
    """
    Calcula a largura das colunas com base no conteúdo mais longo de cada coluna.
    """
    col_widths = []
    
    # Iterar por cada coluna e calcular a largura necessária
    for col in dataframe.columns:
        max_length = pdf.get_string_width(col)  # Largura do nome da coluna
        for value in dataframe[col]:
            max_length = max(max_length, pdf.get_string_width(str(value)))  # Largura do conteúdo da célula
        col_widths.append(max_length + padding)  # Adicionar algum padding

    return col_widths

def generate_pdf(dataframe, title, save_path):
    """
    Gera um arquivo PDF a partir de um DataFrame.
    """
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Título
    pdf.set_font("Arial", size=16)
    pdf.cell(150, 5, txt=title, ln=True, align='C')
    
    # Cabeçalho
    pdf.set_font("Arial", size=12, style='B')

    # Calculando as larguras das colunas
    col_widths = calculate_column_widths(dataframe, pdf)

    # Cabeçalhos das colunas
    for col, width in zip(dataframe.columns, col_widths):
        pdf.cell(width, 10, col, 1, 0, 'C')
    pdf.ln()

    # Dados
    pdf.set_font("Arial", size=10)
    for i in range(len(dataframe)):
        for col, width in zip(dataframe.columns, col_widths):
            pdf.cell(width, 10, str(dataframe.iloc[i][col]), 1, 0, 'C')
        pdf.ln()

    # Salvar PDF
    pdf.output(save_path)
    #st.info(f"PDF '{title}.pdf' foi salvo no diretório atual.")

    # Exibir PDF no Streamlit
    with open(save_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
        st.markdown(pdf_display, unsafe_allow_html=True)

def get_unidades_by_grupo(grupo_id):
    """
    Busca todas as unidades vinculadas ao grupo informado.
    """
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_unidade, nome_unidade, tipo, cidade, estado FROM unidade WHERE id_grupo = %s", (grupo_id,))
    unidades = cursor.fetchall()
    cursor.close()
    conn.close()
    return unidades

def add_setor(nome_setor, g1, g2, g3, g4, selected_unidade_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO setor (nome_setor, g1, g2, g3, g4, id_unidade)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nome_setor, g1, g2, g3, g4, selected_unidade_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_unidades():
    """
    Busca todas as unidades do banco de dados.
    """
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_unidade, nome_unidade FROM unidade")
    unidades = cursor.fetchall()
    cursor.close()
    conn.close()
    return unidades

# Função para atualizar setor
def update_setor(new_name, g1, g2, g3, g4, selected_setor_id):
    conn = create_connection()
    cursor = conn.cursor()
    params = [(new_name, g1, g2, g3, g4, selected_setor_id)]
    cursor.executemany("""
    UPDATE setor
    SET nome_setor = %s, g1 = %s, g2 = %s, g3 = %s, g4 = %s
    WHERE id_setor = %s
    """, params)
    conn.commit()
    cursor.close()
    conn.close()

def Limp():
    st.empty()
    a=0
    b = 30
    while a <b:
        st.write('                ')
        a=a+1

def show_setores_crud():

    st.subheader("Gerenciar Setores")

    with st.container(border=True):
 
        with st.container(border=True):
            menu = ["Clique aqui","Listar Setores", "Adicionar Setores", "Atualizar Setores", "Excluir Setores"]
            Op = st.selectbox("Selecione uma ação relacionada aos SETORES:", menu)
            
            if Op == "Listar Setores":

                st.subheader("Listar Setores por Unidade e Grupo")

                with st.container(border=True):
                    
                    conn = create_connection()
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM setor")
                    setor = cur.fetchall()                    
                    conn.close()

                    grupos = get_all_grupos()

                    # Lista suspensa de grupos
                    grupo_names = [f"{grupo['id_grupo']} - {grupo['nome_grupo']}" for grupo in grupos]
                    selected_grupo = st.selectbox("Selecione o Grupo para listar as Unidades", grupo_names)
                    selected_grupo_id = int(selected_grupo.split(' - ')[0])
                    
                    unidades = get_unidades_by_grupo(selected_grupo_id)

                    # Lista suspensa de unidades vinculadas ao grupo selecionado
                    unidade_names = [f"{unidade['id_unidade']} - {unidade['nome_unidade']}" for unidade in unidades]
                    selected_unidade = st.selectbox("Selecione a Unidade para listar os Setores", unidade_names)
                    selected_unidade_id = int(selected_unidade.split(' - ')[0])
                    n_unid = selected_unidade.split(' - ', 1)[1]

                    setores = get_setores_by_unidade(selected_unidade_id)
                    
                    if not setores:
                        st.warning("Nenhum setor encontrado para a unidade selecionada.")
                        return
              
                    # Exibir o cabeçalho da tabela com os nomes dos campos
                    colunas = st.columns((2, 6, 2, 2, 2, 2, 3))
                    campos = ['ID', 'Setor', 'G1', 'G2', 'G3', 'G4', 'Taxa']

                    # Escreve o cabeçalho
                    for coluna, campo in zip(colunas, campos):
                        coluna.write(campo)

                    # Itera sobre os setores e preenche os dados

                    for setor in setores:

                        # Verifica se 'setor' é um dicionário e possui as chaves esperadas
                        if isinstance(setor, dict) and all(key in setor for key in ['id_setor', 'nome_setor', 'G1', 'G2', 'G3', 'G4', 'taxa']):
                            
                            col1, col2, col3, col4, col5, col6, col7 = st.columns((2, 6, 2, 2, 2, 2, 3))                       
                            col1.write(setor['id_setor'])  # ID do setor
                            col2.write(setor['nome_setor'])  # Nome do setor
                            col3.write(setor['G1'])  # G1
                            col4.write(setor['G2'])  # G2
                            col5.write(setor['G3'])  # G3
                            col6.write(setor['G4'])  # G4
                            col7.write(setor['taxa'])  # Taxa
                        else:
                            st.error("Formato de dados inválido ou chaves ausentes no setor.")
                                    # Reestruturar os dados para evitar problemas de fragmentação

                restructured_data = []

                for setor in setores:
                    if isinstance(setor, dict):
                        registro = {
                            "ID": setor.get("id_setor", ""),
                            "Nome": setor.get("nome_setor", ""),
                            "G1": setor.get("G1", ""),
                            "G2": setor.get("G2", ""),
                            "G3": setor.get("G3", ""),
                            "G4": setor.get("G4", ""),
                            "Taxa": setor.get("taxa", ""),
                            #"ID Unidade": setor.get("id_unidade", "")
                        }
                    elif isinstance(setor, tuple):
                        registro = {
                            "ID": setor[0],
                            "Nome": setor[1],
                            "G1": setor[2],
                            "G2": setor[3],
                            "G3": setor[4],
                            "G4": setor[5],
                            "Taxa": setor[6],
                            #"ID Unidade": setor[7]
                        }
                    else:
                        continue

                    restructured_data.append(registro)

                    # Criar DataFrame com os dados reestruturados
                    df = pd.DataFrame(restructured_data)
                    df = df.astype(str)
                    df.reset_index(drop=True)

                # Botão para gerar PDF
                if st.button("Gerar PDF"):
                    pdf_filename = os.path.join(os.getcwd(), "Unidades_de_Saude.pdf")                   
                    generate_pdf(df, "Setores de =>  "+n_unid, pdf_filename)
                    #st.success("PDF gerado e exibido com sucesso!")
                
        Limp() # Limpa resíduos da página anterior

        if Op == "Adicionar Setores":
            with st.container(border=True):

                unidades = get_all_unidades()

                if unidades:
                    unidade_names = [f"{unidade['id_unidade']} - {unidade['nome_unidade']}" for unidade in unidades]
                    selected_unidade = st.selectbox("Selecione a unidade à qual o setor pertence", unidade_names)
                    selected_unidade_id = int(selected_unidade.split(' - ')[0])

                    op = ["Clique aqui", "Acolhimento", "Triagem", "Consultório", "Medicação", "Sala vermelha", "Sala amarela", "Centro cirúrgico", "UTI", "Enfermaria"]
                    selected_op = st.selectbox("Selecione o Setor:", op)
                    st.write("Setor escolhido =>  "+str(selected_op))
                    nome_setor = selected_op
                    g1 = st.text_input("G1", placeholder="Insira um valor entre 1 e 4 - Isso será usado para o cálculo da Taxa.")
                    g2 = st.text_input("G2", placeholder="Insira um valor entre 1 e 4 - Isso será usado para o cálculo da Taxa.")
                    g3 = st.text_input("G3", placeholder="Insira um valor entre 1 e 4 - Isso será usado para o cálculo da Taxa.")
                    g4 = st.text_input("G4", placeholder="Insira um valor entre 1 e 4 - Isso será usado para o cálculo da Taxa.")
                    #taxa = st.text_input("Taxa")

                    if st.button("Adicionar Setor"):
                        if nome_setor and g1 and g2 and g3 and g4:
                            add_setor(nome_setor, g1, g2, g3, g4, selected_unidade_id)
                            st.success(f"Setor '{nome_setor}' adicionado com sucesso à unidade '{selected_unidade.split(' - ')[1]}'!")
                        else:
                            st.warning("Por favor, preencha todos os campos!")
                else:
                    st.warning("Nenhuma unidade encontrada para vinculação!")                

        if Op == "Atualizar Setores":     # Atualizar setor
            
            with st.container(border=True):
                st.subheader("Ação escolhida = > Atualizar Setor")              

                unidades = get_all_unidades()                     
                
                if not unidades:
                    st.warning("Nenhuma unidade encontrada!")
                    return

                if unidades:
                    unidade_names = [f"{unidade['id_unidade']} - {unidade['nome_unidade']}" for unidade in unidades]
                    selected_unidade = st.selectbox("Selecione a unidade à qual o setor pertence", unidade_names)
                    selected_unidade_id = int(selected_unidade.split(' - ')[0])                    

                setores = get_setores_by_unidade(selected_unidade_id)

                setor = list(setores[0].values())
                
                if setores:

                    # Preencher os campos com os valores atuais
                    st.subheader("Nome atual do Setor =>  "+setor[1])
                    op = ["Clique aqui", "Acolhimento", "Triagem", "Consultório", "Medicação", "Sala vermelha", "Sala amarela", "Centro cirúrgico", "UTI", "Enfermaria"]
                    selected_op = st.selectbox("Manenha ou escolha um novo Setor:" , op)
                    new_name = op

                    if selected_op != "Clique aqui":
                        st.subheader("Tipo de setor alterado para  =>  "+str(selected_op))
                    else:
                        st.write('Escolha um setor')
                    
                    selected_setor_id = int(setor[0])
                    
                    print(setor[0])

                    st.write("Insira um valor entre 1 e 4 - Isso será usado para o cálculo da Taxa.")
                    g1 = st.text_input("G1", setor[2])
                    g2 = st.text_input("G2", setor[3])
                    g3 = st.text_input("G3", setor[4])
                    g4 = st.text_input("G4", setor[5])

                    #taxa = st.text_input("Taxa", value=setor['taxa'])

                    # Botão para atualizar
                    if st.button("Atualizar Setor"):
                        if int(g1) > 4:
                            st.warning('Insira apenas valores entre 1 e 4!')
                        elif int(g2) > 4:
                            st.warning('Insira apenas valores entre 1 e 4!')
                        elif int(g3) > 4:
                            st.warning('Insira apenas valores entre 1 e 4!')
                        elif int(g4) > 4:
                            st.warning('Insira apenas valores entre 1 e 4!')
                        else:
                            update_setor(selected_setor_id, new_name, g1, g2, g3, g4)
                            st.success(f"Setor {new_name} atualizado com sucesso!")
                else:
                    st.warning("Nenhum setor encontrado nesta Unidade!")                    

        if Op == "Excluir Setores":     # Excluir setor

            with st.container(border=True):
                st.subheader("Excluir Setor")  

                unidades = get_all_unidades()
                
                if not unidades:
                    st.warning("Nenhuma unidade encontrada!")
                    return
                
                if unidades:
                    unidade_names = [f"{unidade['id_unidade']} - {unidade['nome_unidade']}" for unidade in unidades]
                    selected_unidade = st.selectbox("Selecione a unidade à qual o setor pertence", unidade_names)
                    selected_unidade_id = int(selected_unidade.split(' - ')[0])

                setores = get_setores_by_unidade(selected_unidade_id)
                
                if setores:
                    setor_names = [f"{setor['id_setor']} - {setor['nome_setor']}" for setor in setores]
                    selected_setor = st.selectbox("Selecione o setor para atualizar", setor_names)

                    # Extrair o ID do setor selecionado
                    selected_setor_id = int(selected_setor.split(' - ')[0])

                    # Botão de exclusão
                    if st.button("Excluir"):
                        delete_setor(selected_setor_id)
                        st.success(f"Setor '{selected_setor.split(' - ')[1]}' excluído com sucesso.")

                else:
                    st.warning("Nenhum setor encontrado nesta Unidade!")      


import streamlit as st
from restrito.utils import create_connection
from fpdf import FPDF
import pandas as pd
import base64
import os

def delete_grupo(grupo_id):
    """
    Exclui o grupo do banco de dados com o ID fornecido.
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM grupo WHERE id_grupo = %s", (grupo_id,))
    conn.commit()
    cursor.close()
    conn.close()

# Função para buscar todos os grupos
def get_all_grupos():
    conn = create_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id_grupo, nome_grupo FROM grupo")
    groups = cur.fetchall()
    cur.close()
    conn.close()
    return groups

def get_unidades_by_grupo(grupo_id):
    """
    Busca todas as unidades pertencentes ao grupo informado.
    """
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_unidade, nome_unidade, tipo, endereco, cep, bairro, cidade, estado, telefone, email, horario FROM unidade WHERE id_grupo = %s", (grupo_id,))
    unidades = cursor.fetchall()
    cursor.close()
    conn.close()
    return unidades

def get_setores_by_unidade(unidade_id):
    """
    Busca todos os setores pertencentes à unidade informada.
    """
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_setor, nome_setor, g1, g2, g3, g4, taxa FROM setor WHERE id_unidade = %s", (unidade_id,))
    setores = cursor.fetchall()
    cursor.close()
    conn.close()
    return setores

def get_group_by_id(group_id):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM grupo WHERE id_grupo = %s", (group_id,))
    group = cursor.fetchone()
    conn.close()
    return group

def update_group(new_name, new_desc, selected_group_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE grupo SET nome_grupo = %s, descricao = %s WHERE id_grupo = %s", (new_name, new_desc, selected_group_id))
    conn.commit()
    conn.close()

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
    Gera um arquivo PDF a partir de um DataFrame e exibe no navegador.
    """
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=16, style='B')
    
    # Título
    pdf.set_font("Arial", size=14)
    pdf.cell(150, 5, txt=title, ln=True, align='C')
    
    # Cabeçalho
    pdf.set_font("Arial", size=10, style='B')

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

def show_grupos_crud():
    st.subheader("Grupos de Unidades de Saúde")
    with st.container():
        menu = ["Clique aqui","Listar Grupos", "Adicionar Grupo", "Atualizar Grupo", "Excluir Grupo"]
        Op = st.selectbox("Selecione uma ação relacionada aos GRUPOS:", menu)
        
        if Op == "Listar Grupos":
            with st.container():

                conn = create_connection()
                cur = conn.cursor()
                cur.execute("SELECT * FROM grupo")
                grupos = cur.fetchall()
                conn.close()

                if not grupos:
                    st.warning("Nenhum grupo encontrado!")
                    return

                colun = st.columns((2,16,13))       
                campos = ['ID', 'Grupo', 'Descrição']
                
                for colun, campos in zip(colun, campos):
                    colun.write(campos)

                for grupo in grupos:
                    col1, col2, col3 = st.columns((2,16,13))
                    col1.write(grupo[0])
                    col2.write(grupo[1])        
                    col3.write(grupo[2])

                    # Reestruturar os dados para evitar problemas de fragmentação
                    restructured_data = []

                    for grupo in grupos:
                        if isinstance(grupo, tuple):
                            registro = {
                                "ID": grupo[0],  # Primeiro elemento da tupla
                                "Nome do Grupo": grupo[1],
                                "Descrição do Grupo": grupo[2],
                            }
                        restructured_data.append(registro)

                    # Tabela de exibição dos grupos
                    df = pd.DataFrame(restructured_data)
                    
                    # Converter para string para evitar problemas de serialização
                    df = df.astype(str) 
                    df.reset_index(drop=True)

                    # Gerar PDF
                    pdf_filename = os.path.join(os.getcwd(), "Grupos_Unidades_de_Saude.pdf")
                    if st.button("Gerar PDF"):                        
                        generate_pdf(df, "Grupos das Unidades de Saúde", pdf_filename)
                        #st.success("PDF gerado e exibido com sucesso!")                    

        if Op == "Adicionar Grupo":
            with st.container(border=True):
                # Inserir novo grupo
                st.subheader("Adicionar Novo Grupo")
                nome_grupo = st.text_input("Nome do Grupo")
                descricao = st.text_area("Descrição")
                
                if st.button("Gravar"):
                    query = f"INSERT INTO grupo (nome_grupo, descricao) VALUES ('{nome_grupo}', '{descricao}')"
                    conn = create_connection()
                    cur = conn.cursor()
                    cur.execute(query)
                    conn.commit()
                    st.success("Grupo adicionado com sucesso!")
            
        if Op == "Atualizar Grupo":
            def update_group_page():
                st.subheader("Atualizar dados do Grupo")
            
                groups = get_all_grupos()

                if groups:
                    group_names = [f"{group['id_grupo']} - {group['nome_grupo']}" for group in groups]
                    selected_group = st.selectbox("Selecione o grupo para atualizar", group_names)
                    
                    # Extrair o ID do grupo selecionado
                    selected_group_id = int(selected_group.split(' - ')[0])
                    
                    # Buscar os dados do grupo selecionado
                    group = get_group_by_id(selected_group_id)

                    if group:
                        # Preencher o campo com o valor atual
                        new_name = st.text_input("Nome do Grupo a ser alterado", value=group['nome_grupo'])
                        new_desc = st.text_input("Descrição a ser alterada", value=group['descricao'])

                        # Botão de confirmação de atualização
                        if st.button("Atualizar Grupo"):
                            update_group(new_name, new_desc, selected_group_id)
                            st.success(f"Grupo {new_name} atualizado com sucesso!")
                else:
                    st.warning("Nenhum grupo encontrado!")

            with st.container(border=True):
                update_group_page()
        
        if Op == "Excluir Grupo":     

            grupos = get_all_grupos()

            if not grupos:
                st.warning("Nenhum grupo encontrado para exclusão.")
                return

            # Lista suspensa de grupos para exclusão
            grupo_names = [f"{grupo['id_grupo']} - {grupo['nome_grupo']}" for grupo in grupos]
            selected_grupo = st.selectbox("Selecione o Grupo que deseja excluir", grupo_names)
            selected_grupo_id = int(selected_grupo.split(' - ')[0])
    
            with st.container(border=True): 

                if st.button("Excluir Grupo"):
                    delete_grupo(selected_grupo_id)
                    st.success(f"Grupo '{selected_grupo.split(' - ')[1]}' excluído com sucesso.")


import streamlit as st
from restrito.utils import create_connection
from fpdf import FPDF
import pandas as pd
import base64
import os

def get_all_groups():
    """
    Recupera todos os grupos da tabela 'grupos'.
    Retorna uma lista de dicionários com 'id' e 'nome' de cada grupo.
    """
    conn = create_connection()  # Conecte-se ao banco de dados
    cursor = conn.cursor(dictionary=True)  # Usa dictionary=True para retornar resultados como dicionário
    cursor.execute("SELECT id_grupo, nome_grupo FROM grupo")
    grupos = cursor.fetchall()  # Recupera todos os registros
    cursor.close()  # Fecha o cursor
    conn.close()  # Fecha a conexão
    return grupos

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

def get_unidade_by_id(unidade_id):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM unidade WHERE id_unidade = %s", (unidade_id,))
    unidade = cursor.fetchone()
    cursor.close()
    conn.close()
    return unidade

def delete_unidade(unidade_id):
    """
    Exclui a unidade do banco de dados com o ID fornecido.
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM unidade WHERE id_unidade = %s", (unidade_id,))
    conn.commit()
    cursor.close()
    conn.close()
        
def update_unidade(selected_unidade_id, novo_nome_unidade, novo_tipo, novo_endereco, novo_bairro, nova_cidade, novo_estado, novo_cep, novo_telefone, novo_email, novo_horario):
    conn = create_connection()
    cursor = conn.cursor()
    query = f"UPDATE unidade SET id_unidade = '{selected_unidade_id}, 'nome_unidade = '{novo_nome_unidade}', tipo = '{novo_tipo}', endereco = '{novo_endereco}', cep = '{novo_cep}', bairro = '{novo_bairro}', cidade = '{nova_cidade}', estado = '{novo_estado}', telefone = '{novo_telefone}', email = '{novo_email}', horario = '{novo_horario}' WHERE id_unidade = {selected_unidade_id}"
    cursor.execute(query)               
    conn.commit()
    cursor.close()

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

def show_unidades_crud():

    st.subheader("Gerenciar Unidades de Saúde")
    with st.container(border=True):
        menu = ["Clique aqui","Listar Unidades", "Adicionar Unidades", "Atualizar Unidades", "Excluir Unidades"]
        Op = st.selectbox("Selecione uma ação relacionada às UNIDADES:", menu)
        
        if Op == "Listar Unidades":

            grupos = get_all_groups()

            if not grupos:
                st.warning("Nenhum grupo encontrado.")
                return
            
            # Lista suspensa de grupos
            grupo_names = [f"{grupo['id_grupo']} - {grupo['nome_grupo']}" for grupo in grupos]
            selected_grupo = st.selectbox("Selecione o Grupo para listar as Unidades", grupo_names)
            selected_grupo_id = int(selected_grupo.split(' - ')[0])

            # Buscar unidades vinculadas ao grupo selecionado
            unidades = get_unidades_by_grupo(selected_grupo_id)

            if not unidades:
                st.warning("Nenhuma unidade encontrada para o grupo selecionado.")
                return

            # Exibir lista de Unidades por Grupo
        
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM unidade")
            unid = cur.fetchall()
            conn.close()

            with st.container(border=True):
                with st.container(border=True):
                    st.write(f"**Grupo selecionado => '{selected_grupo.split(' - ')[2]}':**")
                
                colun = st.columns((2,10,18))       
                campos = ['ID', 'Unidade', 'Endereço']
                for colun, campos in zip(colun, campos):
                    colun.write(campos)

                if not unid:
                    st.warning('Nenhuma Unidade existente no cadastro!')

                for unidades in unid:
                    
                    #print(grupos)
                    col1, col2, col3 = st.columns((2,10,18))
                    col1.write(unidades[0])
                    col2.write(unidades[1])        
                    col3.write(unidades[4])
                    #st.write(f"ID: {grupo[0]}, Nome: {grupo[1]}, Descrição: {grupo[2]}")                            
                
                restructured_data = []

                for unidade in unid:
                    if isinstance(unidade, dict):
                        registro = {
                            "ID Grupo": unidade.get("id_grupo", ""),
                            "ID": unidade.get("id_unidade", ""),
                            "Nome": unidade.get("nome", ""),
                            "Tipo": unidade.get("tipo", ""),
                            "Endereço": unidade.get("endereco", ""),
                            "Bairro": unidade.get("bairro", ""),
                            "Telefone": unidade.get("telefone", ""),
                            "Email": unidade.get("email", ""),
                            "Horário": unidade.get("horario", "")
                            
                        }
                    elif isinstance(unidade, tuple):
                        
                        registro = {
                            "ID Grupo": unidade[2],
                            "ID": unidade[0],
                            "Nome": unidade[1],
                            "Tipo": unidade[3],
                            "Endereço": unidade[4],
                            "Bairro": unidade[6],
                            "Telefone": unidade[9],
                            "Email": unidade[10],
                            "Horário": unidade[11]
                        }
                    else:
                        continue

                    restructured_data.append(registro)

                # Criar DataFrame com os dados reestruturados
                df = pd.DataFrame(restructured_data)
                df = df.astype(str)
                df.reset_index(drop=True)

                # Remover o índice ao exibir a tabela no Streamlit
                #st.table(df.reset_index(drop=True))

                # Gerar PDF
                pdf_filename = os.path.join(os.getcwd(), "Grupos_Unidades_de_Saude.pdf")
                if st.button("Gerar PDF"):                        
                    generate_pdf(df, "Grupos das Unidades de Saúde", pdf_filename)
                    #st.success("PDF gerado e exibido com sucesso!") 

        if Op == "Adicionar Unidades": # Inserir nova Unidade

            def add_unidade(nome, tipo, endereco, cep, bairro, cidade, estado, telefone, email, horario, id_grupo):
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO unidade (nome_unidade, tipo, endereco, cep, bairro, cidade, estado, telefone, email, horario_funcionamento, id_grupo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (nome, tipo, endereco, cep, bairro, cidade, estado, telefone, email, horario, id_grupo))
                conn.commit()
                cursor.close()
                conn.close()
            
            with st.container(border=True):
                
                st.subheader("Adicionar Nova Unidade")

                # Buscar todos os grupos
                grupos = get_all_groups()

                if grupos:
                    grupo_names = [f"{grupo['id_grupo']} - {grupo['nome_grupo']}" for grupo in grupos]
                    selected_grupo = st.selectbox("Selecione o grupo ao qual a unidade pertence", grupo_names)
                    selected_grupo_id = int(selected_grupo.split(' - ')[0])

                    nome_unidade = st.text_input("Nome da Unidade")
                    tipo = st.text_input("Tipo")
                    endereco = st.text_input("Endereço")
                    cep = st.text_input("CEP")
                    bairro = st.text_input("Bairro")
                    cidade = st.text_input("Cidade")
                    estado = st.text_input("Estado")
                    telefone = st.text_input("Telefone")
                    email = st.text_input("Email")
                    horario = st.text_input("Horário de Funcionamento")

                    if st.button("Adicionar Unidade"):
                        if (nome_unidade and tipo and endereco and cep and 
                            bairro and cidade and estado and telefone and email and horario):
                            
                            add_unidade(nome_unidade, tipo, endereco, cep, bairro,
                                        cidade, estado, telefone, email, horario, selected_grupo_id)
                            
                            st.success(f"Unidade '{nome_unidade}' adicionada com sucesso ao grupo '{selected_grupo.split(' - ')[1]}'!")
                        else:
                            st.warning("Por favor, preencha todos os campos.")
                else:
                    st.warning("Nenhum grupo encontrado para vinculação.")

        if Op == "Atualizar Unidades": # Atualizar Unidade

            st.subheader("Atualizar pelo Nome da Unidade")

            with st.container(border=True):
                # Buscar todas as unidades e criar uma lista suspensa

                def get_all_unidades():
                    conn = create_connection()
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("SELECT id_unidade, nome_unidade FROM unidade")
                    unidades = cursor.fetchall()
                    cursor.close()
                    conn.close()
                    return unidades
                
                unidades = get_all_unidades()

                if unidades:
                    unidade_names = [f"{unidade['id_unidade']} - {unidade['nome_unidade']}" for unidade in unidades]
                    selected_unidade = st.selectbox("Selecione a unidade para atualizar", unidade_names)

                    # Extrair o ID da unidade selecionada
                    selected_unidade_id = int(selected_unidade.split(' - ')[0])
                    #print(unidades)

                    unidade = get_unidade_by_id(selected_unidade_id)

                    if unidade:
                        # Preencher os campos com os valores atuais
                        st.subheader("Atualizar Unidade")
                        unidade_id = st.write("ID da Unidade a ser atualizada => "+str(selected_unidade_id))
                        novo_nome_unidade = st.text_input("Novo Nome da Unidade", value=unidade['nome_unidade'])
                        novo_tipo = st.text_input("Novo Tipo" , value=unidade['tipo'])
                        novo_endereco = st.text_input("Novo Endereço", value=unidade['endereco'])
                        novo_bairro = st.text_input("Novo Bairro", value=unidade['bairro'])
                        nova_cidade = st.text_input("Nova Cidade", value=unidade['cidade'])         
                        novo_estado = st.text_input("Novo Estado", value=unidade['estado'])
                        novo_cep = st.text_input("Novo CEP", value=unidade['cep'])
                        novo_telefone = st.text_input("Novo Telefone", value=unidade['telefone'])
                        novo_email = st.text_input("Novo Email", value=unidade['email'])
                        novo_horario = st.text_input("Novo Horário de Funcionamento", value=unidade['horario_funcionamento'])

                        # Botão para atualizar
                        if st.button("Atualizar"):
                            print(novo_estado)
                            #update_unidade(selected_unidade_id, novo_nome_unidade, novo_tipo, novo_endereco, novo_bairro, nova_cidade, novo_estado, novo_cep, novo_telefone, novo_email, novo_horario)
                            #novo_estado_truncated = novo_estado[:max_length]
                            query = query = """UPDATE unidade SET 
                                nome_unidade = %s,
                                tipo = %s,
                                endereco = %s,
                                bairro = %s,
                                cidade = %s,
                                estado = %s,
                                cep = %s,
                                telefone = %s,
                                email = %s,
                                horario_funcionamento = %s
                                WHERE id_unidade = %s"""
                            params = (
                                'novo_nome',
                                'novo_tipo',
                                'novo_endereco',
                                'novo_bairro',
                                'nova_cidade',
                                'RJ',
                                'novo_cep',
                                'novo_telefone',
                                'novo_email',
                                'novo_horario',
                                selected_unidade_id
                            )
                            # Obs.: O input do Estado foi arbitrado devido a um erro não resolvido (Data too long for column 'estado' at row 1) ao gravar as alterações
                            conn = create_connection()  # Conecte-se ao banco de dados
                            cursor = conn.cursor(dictionary=True)  # Usa dictionary=True para retornar resultados como dicionário
                            cursor.execute(query, params)
                            cursor.close()

                            st.success(f"Unidade {novo_nome_unidade} atualizada com sucesso!")
                    else:
                        st.error("Nenhuma Unidade encontrada!")

        if Op == "Excluir Unidades":     # Excluir unidade

            def get_all_unidades():
                conn = create_connection()
                cur = conn.cursor(dictionary=True)
                cur.execute("SELECT id_unidade, nome_unidade FROM unidade")
                unidades = cur.fetchall()
                cur.close()
                conn.close()
                return unidades
    
            # Buscar todas as unidades disponíveis
            unidades = get_all_unidades()

            with st.container(border=True): 

                if not unidades:
                    st.warning("Nenhuma unidade encontrada para exclusão!")
                    return

                # Lista suspensa de unidades para exclusão
                unidade_names = [f"{unidade['id_unidade']} - {unidade['nome_unidade']}" for unidade in unidades]
                selected_unidade = st.selectbox("Selecione a Unidade que deseja excluir", unidade_names)
                selected_unidade_id = int(selected_unidade.split(' - ')[0])

                # Botão de exclusão
                if st.button("Excluir Unidade"):
                    delete_unidade(selected_unidade_id)
                    st.success(f"Unidade '{selected_unidade.split(' - ')[1]}' excluída com sucesso!")


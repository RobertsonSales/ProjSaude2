import streamlit as st
import livre.Querys as Querys
from fpdf import FPDF
import pandas as pd
import os
import tempfile  # Importar para usar diretório temporário

# Função para calcular as larguras das colunas com base no conteúdo
def calculate_column_widths(dataframe, pdf, padding=5):
    col_widths = []
    
    for col in dataframe.columns:
        max_length = pdf.get_string_width(col)
        for value in dataframe[col]:
            max_length = max(max_length, pdf.get_string_width(str(value)))
        col_widths.append(max_length + padding)
    
    return col_widths

# Função para gerar o PDF com base no DataFrame
def generate_pdf(dataframe, save_path):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=16, style='B')

    pdf.cell(0, 10, txt="Relatório de Unidades de Saúde", ln=True, align='C')

    pdf.set_font("Arial", size=8.5)
    col_widths = calculate_column_widths(dataframe, pdf, padding=5)

    for col, width in zip(dataframe.columns, col_widths):
        pdf.cell(width, 10, col, border=1, align='C')
    pdf.ln()

    for row in dataframe.itertuples(index=False):
        for value, width in zip(row, col_widths):
            pdf.cell(width, 10, str(value), border=1, align='C')
        pdf.ln()

    pdf.output(save_path)
    return save_path

def Limp():
    st.empty()
    a=0
    b = 30
    while a <b:
        st.write('                ')
        a=a+1

# Função para exibir a lista e gerar o PDF
def List():
    st.success("UBS no Rio de Janeiro - Você pode obter mais informações clicando em 'Ir à página'.")
    if st.button('Imprimir lista'):
        base = "ubs_rio"
        dados = Querys.Select_Frame(base)
        colunas = ['Unidade', 'Tipo', 'Endereço', 'Bairro', 'Telefone', 'Funcionamento']
        df = pd.DataFrame(dados, columns=colunas)

        # Use o diretório temporário padrão para salvar o PDF
        temp_dir = tempfile.gettempdir()
        save_path = os.path.join(temp_dir, "Relatorio_UBS.pdf")

        # Gera o PDF e salva no caminho especificado
        generate_pdf(df, save_path)
        st.success(f"Arquivo PDF gerado e salvo em: {save_path}")

        # Fornecendo um botão de download para o PDF
        with open(save_path, "rb") as f:
            st.download_button(
                label="Baixar PDF",
                data=f,
                file_name="Relatorio_UBS.pdf",
                mime="application/pdf"
            )

    with st.container():
        colun = st.columns((2, 16, 6, 5))
        campos = ['Cod', 'Unidade', 'Telefone', 'Pesquisar']

        for colun, campos in zip(colun, campos):
            colun.write(campos)

        for item in (Querys.Select6()):
            col1, col2, col5, col6 = st.columns((2, 16, 6, 5))
            col1.write(item[11])
            col2.write(item[0])
            col5.write(item[8])

            query = item[0].strip()
            search_url = f"https://www.google.com/search?q={query}"
            col6.write(f'<a href="{search_url}" target="_blank">Ir à página</a>', unsafe_allow_html=True)
        Limp()


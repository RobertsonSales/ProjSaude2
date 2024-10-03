import services.database as db
import streamlit as st 

class Unid:
    def __init__(self, Id_Unid, NOME_FANTASIA, LOGRADOURO, NUMERO, BAIRRO, CEP, TELEFONE, EMAIL, HORARIO, TIPO_GESTAO, LATITUDE, LONGITUDE):
        self.ID = Id_Unid
        self.nome = NOME_FANTASIA
        self.endereco = LOGRADOURO
        self.numero = NUMERO
        self.telefone = TELEFONE
        self.cep = CEP
        self.bairro = BAIRRO
        self.email = EMAIL
        self.hor = HORARIO
        self.gest = TIPO_GESTAO
        self.lat = LATITUDE
        self.long = LONGITUDE


# função para selecionar apenas um registros no banco de dados
def sel_id(item):
  con, cursor = db.create_connection()
  cursor.execute("""SELECT * FROM upas_rio WHERE Id_Unid = '%s'"""% (item[11]))
  recset = cursor.fetchall()
  rows = []
  if not recset:
    st.warning('Cliente inexistente na base!!!')
    return
  else:
    for rec in recset:
      rows.append(rec)
      #print(rec)
      return rows

def Select_Frame(base): # Lista compacta de UPAs 24h
  con, cursor = db.create_connection()
  cursor.execute("SELECT NOME_FANTASIA, TIPO_GESTAO, LOGRADOURO, BAIRRO, TELEFONE, HORARIO FROM "+str(base))
  recset = cursor.fetchall()
  rows = []
  for rec in recset:
    rows.append(rec)
  return rows

def Select(): # Lista de UPAs 24h
  con, cursor = db.create_connection()
  cursor.execute("""SELECT * FROM upas_rio """)
  recset = cursor.fetchall()
  rows = []
  for rec in recset:
    rows.append(rec)
  return rows

def Select1(): # Lista de CER 24h
  con, cursor = db.create_connection()
  cursor.execute("""SELECT * FROM cer_rio """)
  recset = cursor.fetchall()
  rows = []
  for rec in recset:
    rows.append(rec)
  return rows

def Select2(): # Lista de hospitais estaduais
  con, cursor = db.create_connection()
  cursor.execute("""SELECT * FROM hosp_est_rio """)
  recset = cursor.fetchall()
  rows = []
  for rec in recset:
    rows.append(rec)
  return rows

def Select3(): # Lista de hospitais municipais
  con, cursor = db.create_connection()
  cursor.execute("""SELECT * FROM hosp_mun_rio """)
  recset = cursor.fetchall()
  rows = []
  for rec in recset:
    rows.append(rec)
  return rows

def Select4(): # Lista de Clínicas da Família
  con, cursor = db.create_connection()
  cursor.execute("""SELECT * FROM cli_fam_rio """)
  recset = cursor.fetchall()
  rows = []
  for rec in recset:
    rows.append(rec)
  return rows

def Select5(): # Lista de Policlínicas
  con, cursor = db.create_connection()
  cursor.execute("""SELECT * FROM polic_rio """)
  recset = cursor.fetchall()
  rows = []
  for rec in recset:
    rows.append(rec)
  return rows

def Select6(): # Lista de Unidades Básicas de Saúde 
  con, cursor = db.create_connection()
  cursor.execute("""SELECT * FROM unid_bas_rio """)
  recset = cursor.fetchall()
  rows = []
  for rec in recset:
    rows.append(rec)
  return rows

def Select7(): # Lista de Unidades de Referência 
  con, cursor = db.create_connection()
  cursor.execute("""SELECT * FROM c_ref_rio """)
  recset = cursor.fetchall()
  rows = []
  for rec in recset:
    rows.append(rec)
  return rows

def Select8(): # Lista de CAPS 
  con, cursor = db.create_connection()
  cursor.execute("""SELECT * FROM caps_rio """)
  recset = cursor.fetchall()
  rows = []
  for rec in recset:
    rows.append(rec)
  return rows


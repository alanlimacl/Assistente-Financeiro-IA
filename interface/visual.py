import streamlit as st
import sqlite3
import pandas as pd

from app.config import BANCO_DADOS
from interface.pagina_chatbot import chat_bot
from interface.pagina_resumo import grafico_resumo
from interface.pagina_categoria import grafico_categoria


st.set_page_config(page_title="Agente Financeiro IA",
                   page_icon="💰", 
                   layout='wide')


def iniciar_banco_dados():
    conexao = sqlite3.connect(BANCO_DADOS)
    banco_dados = pd.read_sql_query("SELECT * FROM controle_financeiro", conexao)
    conexao.close()

    return banco_dados


st.header("Agente Financeiro IA")

with st.sidebar:
    st.title("Navegação", text_alignment='left')
    pagina = st.radio("Ir para:", ['Chatbot', 'Resumo', 'Gastos por Categoria'])
    
    banco_dados = iniciar_banco_dados()
    

if pagina == 'Chatbot':
    chat_bot()
        
        
elif pagina == 'Resumo':
    grafico_resumo(iniciar_banco_dados)
        
        
elif pagina == 'Gastos por Categoria':
    grafico_categoria(iniciar_banco_dados)


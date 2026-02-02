import streamlit as st
import sqlite3
import os
import pandas as pd
from agente_agno import agente_financeiro
import requests
from datetime import datetime
import plotly.express as px
from utils import MESES_PT

st.set_page_config(page_title="Agente Financeiro IA", page_icon="💰", layout='wide')

def init_bd():
    BD_PATH = os.path.join('banco_dados','dados_user_Alan.db')

    conexao = sqlite3.connect(BD_PATH)
    banco_dados = pd.read_sql_query("SELECT * FROM controle_financeiro", conexao)
    conexao.close()

    return banco_dados


st.header("Agente Financeiro IA")

with st.sidebar:
    st.title("Navegação", text_alignment='left')
    pagina = st.radio("Ir para:", ['Chatbot', 'Resumo', 'Gastos por Categoria'])
    
    banco_dados = init_bd()
    

if pagina == 'Chatbot':
    st.write("Informe seus gastos e categorize. Estou aqui pra te ajudar a entender para onde seu dinheiro está indo.")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        st.chat_message(msg['role']).write(msg['content'])
        
    if prompt := st.chat_input():
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        st.chat_message('user').write(prompt)
        
        with st.spinner('O agente está pensando...'):
            try:
                resposta = requests.post(
                    'http://localhost:8000/perguntar',
                    json={'text':prompt}
                )
                
                if resposta.status_code == 200:
                    dados = resposta.json()
                    resposta_ia = dados['text']
                    # st.success('Reposta recebida')
                    st.session_state.messages.append({'role': 'assistent', 'content': resposta})
                    st.chat_message('assistant').write(resposta_ia)
                    
                else:
                    st.error('Erro no servidor da API')
                    
            except Exception as e:
                st.error(f'Falha na conexão: {e}')
                
            
        
    
elif pagina == 'Resumo':
    st.write('Aqui você encontra um resumo dos gastos por categoria para visualizar melhor seus hábitos financeiros.')
    
    if not banco_dados.empty:
        
        coluna_data = banco_dados.columns[5]
        
        banco_dados[coluna_data] = pd.to_datetime(banco_dados[coluna_data])
        banco_dados['mes_ano'] = banco_dados[coluna_data].dt.to_period('M')
        
        meses = sorted(banco_dados['mes_ano'].unique(), reverse=True)
        mes_atual = datetime.now().strftime('%Y/%m')
        
        meses_label = {
            mes: f'{MESES_PT[mes.month]}/{mes.year}'
            for mes in meses
        }
        
        try:
            indice_padrao = meses.index(mes_atual)
        except ValueError:
            indice_padrao = 0
        
        mes_selecionado = st.sidebar.selectbox('Selecione o Mês:',options=list(meses_label.keys()), format_func= lambda x: meses_label[x])
        
        banco_dados_filtrado = banco_dados[banco_dados['mes_ano'] == mes_selecionado]
        
        coluna1, coluna2, coluna3 = st.columns(3)

        total_gasto = banco_dados_filtrado['valor'].sum()
        quantidade = len(banco_dados_filtrado)
        maior_gasto = banco_dados_filtrado['valor'].max()
        
        coluna1.metric('Gasto Total', f'R$ {total_gasto:,.2f}')
        coluna2.metric('Qtd. Transações', quantidade)
        coluna3.metric('Maior Gasto', f'R$ {maior_gasto:,.2f}')

        st.markdown('---')
        fig_hist = px.bar(
            banco_dados_filtrado.sort_values(coluna_data),
            x=coluna_data,
            y='valor',
            title=f'Evolução Diária em {mes_selecionado}')
        st.plotly_chart(fig_hist, width='stretch')
        
        
elif pagina == 'Gastos por Categoria':
    st.write('Aqui você encontra um resumo dos gastos por categoria para visualizar melhor seus hábitos financeiros')
    
    if not banco_dados.empty:
        
        coluna_data = banco_dados.columns[5]
        
        banco_dados[coluna_data] = pd.to_datetime(banco_dados[coluna_data]) # dayfirst=True
        banco_dados['mes_ano'] = banco_dados[coluna_data].dt.to_period('M')
        
        meses = sorted(banco_dados['mes_ano'].unique(), reverse=True)
        mes_atual = datetime.now().strftime('%Y/%m')
        
        meses_label = {
            mes: f'{MESES_PT[mes.month]}/{mes.year}'
            for mes in meses
        }
        
        try:
            indice_padrao = meses.index(mes_atual)
        except ValueError:
            indice_padrao = 0
        
        mes_selecionado = st.sidebar.selectbox('Selecione o Mês:',options=list(meses_label.keys()), format_func= lambda x: meses_label[x])
        
        banco_dados_filtrado = banco_dados[banco_dados['mes_ano'] == mes_selecionado]
        
        coluna1, coluna2, coluna3 = st.columns(3)

        total_gasto = banco_dados_filtrado['valor'].sum()
        quantidade = len(banco_dados_filtrado)
        maior_gasto = banco_dados_filtrado['valor'].max()
           
        fig_pie = px.pie(banco_dados_filtrado, values='valor', names='categoria', hole=0.3)
        st.plotly_chart(fig_pie, width='stretch')
    


# if __name__ == '__main__':
#     bd = init_bd()
#     print(bd.info())
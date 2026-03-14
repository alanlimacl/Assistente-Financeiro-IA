import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import requests

from app.uteis.formatadores import MESES_PT

URL = "http://localhost:8000"

def buscar_dados_financas():
    """Busca todo o histórico de gastos do usuário logado na API."""
    access_token = st.session_state.get('access_access_token')
    
    if not access_token:
        st.warning("Você precisa fazer login para ver as categorias.")
        return pd.DataFrame()

    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'data_inicio': '2000-01-01', 'data_final': '2100-12-31'}

    try:
        resposta = requests.get(f"{URL}/financas/consultar-gasto", headers=headers, params=params)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            return pd.DataFrame(dados.get('gastos', []))
        else:
            return pd.DataFrame()
    except Exception:
        return pd.DataFrame()

def grafico_categoria():
    st.write('Aqui você encontra um resumo dos gastos por categoria para visualizar melhor seus hábitos financeiros.')
    
    banco_dados = buscar_dados_financas()
    
    if not banco_dados.empty:
        coluna_data = 'data'
        
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
        
        mes_selecionado = st.sidebar.selectbox('Selecione o Mês:', options=list(meses_label.keys()), format_func=lambda x: meses_label[x])
        
        banco_dados_filtrado = banco_dados[banco_dados['mes_ano'] == mes_selecionado]
        
        # Agrupando os valores por categoria para o gráfico de pizza não ficar bagunçado
        dados_pizza = banco_dados_filtrado.groupby('categoria')['valor'].sum().reset_index()
           
        fig_pie = px.pie(dados_pizza, values='valor', names='categoria', hole=0.3, title=f"Divisão de Gastos - {mes_selecionado}")
        
        # Ajustei o width='stretch' para use_container_width=True que é o padrão atual do Streamlit
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Nenhum gasto encontrado para gerar o gráfico de categorias.")
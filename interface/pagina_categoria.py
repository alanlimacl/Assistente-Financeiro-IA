import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

from app.uteis.formatadores import MESES_PT

def grafico_categoria(banco_dados):
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
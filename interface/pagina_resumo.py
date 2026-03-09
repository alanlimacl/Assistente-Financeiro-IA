import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

from app.uteis.formatadores import MESES_PT


def grafico_resumo(banco_dados):
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
        
        banco_dados_grafico = banco_dados_filtrado.sort_values(coluna_data).copy()
        banco_dados_grafico['Data'] = banco_dados_grafico[coluna_data].dt.strftime('%d/%m/%Y')
        banco_dados_grafico = banco_dados_grafico.rename(columns={'valor': 'Valor'})

        # 2. Criamos o gráfico usando a nova coluna de texto
        fig_hist = px.bar(
            banco_dados_grafico,
            x='Data',  # Usamos a string em vez do datetime puro
            y='Valor',
            title=f'Evolução Diária em {mes_selecionado}'
        )
        
        # 3. Forçamos o Plotly a tratar o Eixo X como Categoria (desliga a "régua de tempo")
        fig_hist.update_xaxes(type='category')
        
        st.plotly_chart(fig_hist, width='stretch')
        
    # Criação da Lista de Gastos da Aba Resumo
    st.markdown('---')
    st.subheader(f'Detalhes dos Gastos - {mes_selecionado}')
    
    tabela_exibicao = banco_dados_filtrado.copy()
    
    colunas_amostra = {
        coluna_data: 'Data',
        'item': 'Item',
        'categoria': 'Categoria',
        'metodo_pagamento': 'Forma de Pagamento',
        'valor': 'Valor (R$)'
    }
    
    tabela_exibicao = tabela_exibicao[list(colunas_amostra.keys())] # Filtrando apenas colunas do dicionário
    tabela_exibicao = tabela_exibicao.rename(columns=colunas_amostra) # Renomeando os nomes das colunas
    
    tabela_exibicao['Data'] = pd.to_datetime(tabela_exibicao['Data']).dt.strftime('%d/%m/%Y')
    
    tabela_exibicao = tabela_exibicao.iloc[::-1]
    
    st.dataframe(tabela_exibicao, hide_index=True, use_container_width=True) # Esconde a coluna de indices (0, 1, 2) e Ocupar a tela toda
    
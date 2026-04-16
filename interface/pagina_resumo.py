import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
import requests

from app.uteis.formatadores import MESES_PT

URL = "http://localhost:8000"

def buscar_dados_financas():
    """Busca todo o histórico de gastos do usuário logado na API."""
    access_token = st.session_state.get('access_token')
    
    if not access_token:
        st.warning("Você precisa fazer login para ver o resumo.")
        return pd.DataFrame()

    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Colocamos um período amplo para o banco trazer tudo
    params = {
        'data_inicio': '2000-01-01', 
        'data_final': '2100-12-31'
    }

    try:
        resposta = requests.get(f"{URL}/financas/consultar-gasto", headers=headers, params=params)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            lista_gastos = dados.get('gastos', [])
            
            return pd.DataFrame(lista_gastos)
            
        elif resposta.status_code == 404:
            return pd.DataFrame() # Retorna vazio se não tiver gastos ainda
            
        else:
            st.error("Erro ao carregar os dados do servidor.")
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"Falha na conexão com a API: {e}")
        return pd.DataFrame()


# ATENÇÃO: Removemos o parâmetro (banco_dados) daqui!
def grafico_resumo():
    
    st.header('Resumo dos seus Gastos')
    st.write('Aqui você encontra um resumo dos gastos para visualizar melhor seus hábitos financeiros.')

    # O Pandas cria a tabela a partir do JSON da API perfeitamente!
    banco_dados = buscar_dados_financas()

    if not banco_dados.empty:
        # Puxando pelo nome exato da chave que vem da API
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

        fig_hist = px.bar(
            banco_dados_grafico,
            x='Data', 
            y='Valor',
            title=f'Evolução Diária em {mes_selecionado}'
        )
        
        fig_hist.update_xaxes(type='category')
        st.plotly_chart(fig_hist, width='stretch')
        
        # Criação da Lista de Gastos
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
        
        tabela_exibicao = tabela_exibicao[list(colunas_amostra.keys())] 
        tabela_exibicao = tabela_exibicao.rename(columns=colunas_amostra) 
        
        tabela_exibicao['Data'] = pd.to_datetime(tabela_exibicao['Data']).dt.strftime('%d/%m/%Y')
        tabela_exibicao = tabela_exibicao.iloc[::-1]
        
        st.dataframe(tabela_exibicao, hide_index=True, width='stretch') 
    else:
        st.info("Nenhum gasto encontrado no seu histórico. Fale com o seu Assistente para adicionar!")
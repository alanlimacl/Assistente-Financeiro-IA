import streamlit as st
from time import sleep

from interface.pagina_chatbot import chat_bot
from interface.pagina_resumo import grafico_resumo
from interface.pagina_categoria import grafico_categoria

def logout(cookie_controller):
    """Limpa os dados da sessão."""
    st.session_state.authenticated = False
    
    st.session_state.access_token = None
    st.session_state.refresh_token = None
    st.session_state.username = None
    
    cookie_controller.remove('auth_token')
    cookie_controller.remove('refresh_token')
    cookie_controller.remove('auth_user')
 

def exibir_dashboard(cookie_controller):
    """Renderiza a interface principal do assistente financeiro."""
    # st.header("Agente Financeiro IA")

    with st.sidebar:
        # Saudação e botão de Sair
        st.title(f"Bem-vindo, {st.session_state.username}!")
        st.button("Sair", on_click=logout, args=(cookie_controller,))
        st.markdown("---")
        
        # Navegação
        st.title("Navegação", anchor=False)
        pagina = st.radio("Ir para:", ['Chatbot', 'Resumo', 'Gastos por Categoria'])
        

    # Rotas das páginas chamando as funções vazias
    if pagina == 'Chatbot':
        chat_bot()
            
    elif pagina == 'Resumo':
        grafico_resumo()
            
    elif pagina == 'Gastos por Categoria':
        grafico_categoria()
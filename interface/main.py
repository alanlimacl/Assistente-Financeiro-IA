import streamlit as st
from interface.autorizacao import exibir_tela_login
from dashboard import exibir_dashboard
from streamlit_cookies_controller import CookieController


st.set_page_config(page_title="Agente Financeiro IA",
                   page_icon="💰", 
                   layout='wide')

cookie_controller = CookieController()

# ==========================================
# 1. INICIALIZAÇÃO CORRETA DAS GAVETAS
# ==========================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    
if "access_token" not in st.session_state: # Mudamos de 'token' para 'access_token'
    st.session_state.access_token = None

if "refresh_token" not in st.session_state: # Adicionamos a gaveta do refresh
    st.session_state.refresh_token = None
    
if "username" not in st.session_state:
    st.session_state.username = None


if not st.session_state.authenticated:
    access_token_salvo = cookie_controller.get('auth_token')
    refresh_token_salvo = cookie_controller.get('refresh_token')
    usuario_salvo = cookie_controller.get('auth_user')

    # Se achar, coloca nas gavetas com os nomes exatos que o app espera
    if access_token_salvo and refresh_token_salvo:
        st.session_state.access_token = access_token_salvo
        st.session_state.refresh_token = refresh_token_salvo
        st.session_state.username = usuario_salvo
        st.session_state.authenticated = True

# ==========================================
# 3. ROTEAMENTO DE TELAS
# ==========================================
if not st.session_state.authenticated:
    exibir_tela_login(cookie_controller)
else:
    exibir_dashboard(cookie_controller)
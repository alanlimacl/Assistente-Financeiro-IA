import streamlit as st
from interface.autorizacao import exibir_tela_login
from dashboard import exibir_dashboard
from streamlit_cookies_controller import CookieController


st.set_page_config(page_title="Agente Financeiro IA",
                   page_icon="💰", 
                   layout='wide')

cookie_controller = CookieController()

cookie_token = cookie_controller.get('auth_token')
cookie_user = cookie_controller.get('auth_user')

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    
if "token" not in st.session_state:
    st.session_state.token = None
    
if "username" not in st.session_state:
    st.session_state.username = None

if cookie_token and not st.session_state.authenticated:
    st.session_state.token = cookie_token
    st.session_state.username = cookie_user
    st.session_state.authenticated = True

# Roteamento de telas
if not st.session_state.authenticated:
    exibir_tela_login(cookie_controller)
    
else:
    exibir_dashboard(cookie_controller)
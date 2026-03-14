import streamlit as st
import requests
from time import sleep

# Configuração da URL do seu backend FastAPI
FASTAPI_URL = "http://localhost:8000"

# Inicializa as variáveis de sessão se não existirem
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    
if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = None

if "username" not in st.session_state:
    st.session_state.username = None


def login_user(username, password, cookie_controller):
    """Faz a requisição de login para o FastAPI."""
    # O FastAPI com OAuth2PasswordRequestForm espera 'username' e 'password' via form-data
    data = {"username": username, "password": password}
    try:
        response = requests.post(f"{FASTAPI_URL}/autenticador/login", data=data)
        
        if response.status_code == 200:
            token_data = response.json()
            nome_usuario = token_data.get('nome', username)
            
            access_token = token_data.get('access_token')
            refresh_token = token_data.get('refresh_token')
            
            st.session_state.access_token = access_token
            st.session_state.refresh_token = refresh_token
            
            
            st.session_state.authenticated = True
            st.session_state.username = nome_usuario
            
            cookie_controller.set('auth_token', access_token)
            cookie_controller.set('refresh_token', refresh_token)
            cookie_controller.set('auth_user', nome_usuario)
            
            sleep(0.5)
            
            st.rerun() # Recarrega a página para atualizar a interface
            
        else:
            st.error("Usuário ou senha incorretos.")
            
    except requests.exceptions.ConnectionError:
        st.error("Erro de conexão com o servidor FastAPI. Verifique se ele está rodando.")


def register_user(nome, email, senha):
    """Faz a requisição para criar um novo usuário no FastAPI."""
    json_data = {"nome": nome, "email": email, "senha": senha}
    
    try:
        response = requests.post(f"{FASTAPI_URL}/autenticador/criar-conta", json=json_data)
        
        if response.status_code == 200 or response.status_code == 201:
            st.success("Usuário criado com sucesso! Agora você pode fazer o login.")
            
        elif response.status_code == 401:
            st.warning("Este e-mail de usuário já está em uso.")
            
        else:
            st.error("Erro ao criar usuário.")
            
    except requests.exceptions.ConnectionError:
        st.error("Erro de conexão com o servidor FastAPI.")


def exibir_tela_login(cookie_controller):
    """Renderiza a interface de login e registro no Streamlit."""
    st.title("Assistente Financeiro Pessoal")
    st.write("Faça login ou crie uma conta para acessar seu controle financeiro.")
    
    # Abas para separar Login de Criação de Conta
    tab_login, tab_register = st.tabs(["Login", "Criar Conta"])
    
    with tab_login:
        with st.form("login_form"):
            st.subheader("Entrar")
            log_user = st.text_input("Usuário")
            log_pass = st.text_input("Senha", type="password")
            submit_login = st.form_submit_button("Entrar")
            
            if submit_login:
                if log_user and log_pass:
                    login_user(log_user, log_pass, cookie_controller)
                else:
                    st.warning("Preencha todos os campos.")
                    
    with tab_register:
        with st.form("register_form"):
            st.subheader("Novo Usuário")
            reg_nome = st.text_input("Digite seu nome")
            reg_email = st.text_input("Escolha seu e-mail")
            reg_senha = st.text_input("Escolha uma senha", type="password")
            
            submit_register = st.form_submit_button("Criar Conta")
            
            if submit_register:
                if reg_nome and reg_email and reg_senha:
                    register_user(reg_nome, reg_email, reg_senha)
                else:
                    st.warning("Preencha todos os campos.")

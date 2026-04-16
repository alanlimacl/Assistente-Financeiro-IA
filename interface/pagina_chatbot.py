import streamlit as st
import requests

URL = "http://localhost:8000"

def renovar_token_silenciosamente() -> bool:
    """Bate na rota do FastAPI com o refresh_token e atualiza a chave de acesso."""
    refresh_token = st.session_state.get('refresh_token')

    if not refresh_token:
        return False
    
    try:
        reposta = requests.post(
            f"{URL}/autenticador/refresh-token",
            json={'refresh_token': refresh_token}
        )

        if reposta.status_code == 200:
            novo_access_token = reposta.json().get('access_token')
            
            st.session_state['access_token'] = novo_access_token
            return True
        
        else:
            return False

    except Exception:
        return False
    
    
def chat_bot():
    
    st.header('Agente Financeiro')
    st.write("Informe seus gastos e categorize. Estou aqui pra te ajudar a entender para onde seu dinheiro está indo.")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        st.chat_message(msg['role']).write(msg['content'])
        
    if prompt := st.chat_input("Digite sua mensagem..."):
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        st.chat_message('user').write(prompt)
        
        with st.spinner('O agente está pensando...'):
            
            with st.chat_message('assistant'):
                placeholder = st.empty()
                
                
                def fazer_requisicao_agente(token_usado):
                    headers = {'Authorization': f'Bearer {token_usado}'}
                    
                    return requests.post(
                        f"{URL}/agente/perguntar",
                        json={'text': prompt},
                        headers=headers,
                        stream=True
                    )
                
                try:
                    # TENTATIVA 1: Usa o token atual (que pode estar expirado)
                    resposta = fazer_requisicao_agente(st.session_state.get('access_token'))
                    
                    # A MÁGICA ACONTECE AQUI: Deu 401? Pausa tudo e renova!
                    if resposta.status_code == 401:
                        sucesso_renovacao = renovar_token_silenciosamente()
                        
                        if sucesso_renovacao:
                            # TENTATIVA 2: Refaz a pergunta com o Token Novo!
                            resposta = fazer_requisicao_agente(st.session_state.get('access_token'))
                        else:
                            st.error("Sua sessão expirou de vez. Por favor, faça login novamente.")
                            st.stop() # Para a execução aqui
                    
                    # Processando o texto se a requisição deu certo (seja na 1ª ou na 2ª tentativa)
                    if resposta.status_code == 200:
                        resposta_completa = ''
                        
                        for chunk in resposta.iter_content(chunk_size=None):
                            if chunk:
                                
                                resposta_completa += chunk.decode('utf-8')
                                texto_limpo = resposta_completa.replace('$', r'\$')
                                placeholder.markdown(texto_limpo)
                                
                        # Salva a resposta no histórico da tela
                        st.session_state.messages.append({'role': 'assistant', 'content': texto_limpo})
                        
                    else:
                        st.error("Ops, o Assistente deu uma travada. Tente novamente.")
                        
                except Exception as e:
                    st.error(f"Falha na conexão: {e}")
                    
import streamlit as st
import requests


def chat_bot():
    st.write("Informe seus gastos e categorize. Estou aqui pra te ajudar a entender para onde seu dinheiro está indo.")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        st.chat_message(msg['role']).write(msg['content'])
        
    if prompt := st.chat_input():
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        st.chat_message('user').write(prompt)
        
        with st.spinner('O agente está pensando...'):
            
            with st.chat_message('assistant'):
                placeholder = st.empty()
                resposta_completa = ''
                
                try:
                    resposta = requests.post(
                        'http://localhost:8000/perguntar',
                        json={'text':prompt},
                        stream=True
                    )
                    
                    for chunk in resposta.iter_content(chunk_size=None):
                        if chunk:
                            texto = chunk.decode('utf-8')
                            resposta_completa += texto
                            
                            placeholder.write(resposta_completa)
                            
                    st.session_state.messages.append({'role': 'assistant', 'content': resposta_completa})
                    
                except Exception as e:
                    st.error(f'Falha na conexão: {e}')
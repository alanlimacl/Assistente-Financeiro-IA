from datetime import datetime
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv

from app.config import MODELO_IA
from app.agente_agno.prompts import prompt
from app.config import BANCO_DADOS


load_dotenv()

modelo = OpenAIChat(id=MODELO_IA)

def montar_prompt():
    data_atual = datetime.now().strftime("%Y-%m-%d")
    return prompt.replace("{DATA_ATUAL}", data_atual)

def criar_agente(modelo_ia: OpenAIChat, ferramentas_com_token: list, id_usuario) -> Agent:
    """Cria uma nova instância do Agente já configurada com as ferramentas 
    específicas do usuário que fez a requisição."""
    
    return Agent(model=OpenAIChat(id=modelo_ia),
                name='Agente Financeiro',
                
                session_id=f'usuario_{id_usuario}',
                db=SqliteDb(db_file=BANCO_DADOS),
                
                add_session_state_to_context=True,
                
                tools=ferramentas_com_token,
                
                instructions=montar_prompt(),
                add_history_to_context=True,
                num_history_messages=5,
                
                enable_user_memories=False,
                add_memories_to_context=False,
                
                debug_mode=True
                )    

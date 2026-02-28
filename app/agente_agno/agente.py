from agno.agent import Agent
from dotenv import load_dotenv
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from app.ferramentas import consultar_gastos, adicionar_gastos, remover_gastos, somar_gastos_periodo
from app.config import MODELO_IA, BANCO_DADOS
from app.agente_agno.prompts import prompt
from datetime import datetime


load_dotenv()

modelo = OpenAIChat(id=MODELO_IA)

banco_dados = SqliteDb(id='agente_financeiro', db_file=BANCO_DADOS)

def montar_prompt():
    data_atual = datetime.now().strftime("%Y-%m-%d")
    return prompt.replace("{DATA_ATUAL}", data_atual)


agente = Agent(model=modelo,
                name='Agente Financeiro',
                session_id='Financeiro',
                add_session_state_to_context=True,
                tools=[adicionar_gastos, consultar_gastos, remover_gastos, somar_gastos_periodo],
                db=banco_dados,
                instructions=montar_prompt(),
                add_history_to_context=True,
                num_history_messages=5,
                enable_user_memories=False,
                add_memories_to_context=False,
                debug_mode=True)    


def pergunta_agente(input:str):
    resposta = agente.run(input)
    mensagem_resposta = resposta.content
    
    return mensagem_resposta


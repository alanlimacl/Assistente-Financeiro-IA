from agno.agent import Agent
from dotenv import load_dotenv
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS

from ferramentas import consultar_gastos, adicionar_gastos, remover_gastos
from utils import prompt
import getpass
import socket

usuario_os = getpass.getuser()  
nome_pc = socket.gethostname()
nome_usuario_pc = f'{usuario_os}@{nome_pc}'

load_dotenv()


def agente_financeiro(input:str):

    modelo = OpenAIChat(id="gpt-5-mini")

    banco_dados = SqliteDb(id='agente_financeiro', db_file=f'banco_dados/dados_user_{usuario_os}.db')

    agente = Agent(model=modelo,
                name='Agente Financeiro',
                user_id=nome_usuario_pc,
                session_id='Financeiro',
                add_session_state_to_context=True,
                tools=[adicionar_gastos, consultar_gastos, remover_gastos],
                db=banco_dados,
                instructions=prompt,
                add_history_to_context=True,
                num_history_messages=5,
                enable_user_memories=True,
                add_memories_to_context=True,
                debug_mode=True)        

    resposta = agente.run(input)
    mensagem_resposta = resposta.content
    
    print(mensagem_resposta)
    return mensagem_resposta


if __name__ == '__main__':    
    while True:
        pergunta = input('Você: ')
        
        if pergunta.lower().strip() == 'sair':
            break
        
        agente_financeiro(pergunta)
    
# return mensagem


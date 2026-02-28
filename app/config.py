import os 
from pathlib import Path
from dotenv import load_dotenv
import sqlite3


load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODELO_IA = os.getenv('MODELO_IA')

BASE_ARQUIVO = Path(__file__).resolve().parent.parent
BD_NOME = os.getenv('NOME_BANCO_DADOS')
BD_PASTA = BASE_ARQUIVO / 'banco_dados'
BANCO_DADOS = BD_PASTA / BD_NOME

os.makedirs(BD_PASTA, exist_ok=True)


def inicializar_banco():
    try:
        os.makedirs(os.path.dirname(BD_PASTA), exist_ok=True)
        
        conexao = sqlite3.connect(BANCO_DADOS)
        cursor = conexao.cursor()
    
        cursor.execute("""CREATE TABLE IF NOT EXISTS controle_financeiro (
            id_gasto INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            valor FLOAT NOT NULL,
            categoria TEXT NOT NULL,
            metodo_pagamento TEXT NOT NULL,
            data TEXT NOT NULL)""")
    
        conexao.commit()
        conexao.close()
        
    except sqlite3.OperationalError as e:
        return(f"Erro de Conexão com o Banco de Dados: {e}")

    return "Verificação realizada com sucesso!"


inicializar_banco()



if __name__ == "__main__":
    print(f"✅ Raiz do Projeto: {BASE_ARQUIVO}")
    print(f"✅ Caminho do Banco: {BD_PASTA}")
    print(f'✅ Nome do Banco: {BD_NOME}')
    print(f"✅ Modelo Escolhido: {MODELO_IA}")
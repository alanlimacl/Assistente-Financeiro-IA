import os
from pathlib import Path

MESES_PT = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro'
}

# 1. Pega a pasta onde está o arquivo uteis.py (pasta 'app')
PASTA_APP = os.path.dirname(os.path.abspath(__file__))

# 2. Sobe um nível para a raiz do projeto (pasta 'ASSISTENTE_FINANCEIRO')
RAIZ_PROJETO = os.path.dirname(PASTA_APP)

# 3. Monta o caminho fixo para a pasta banco_dados
PASTA_BANCO = os.path.join(RAIZ_PROJETO, 'banco_dados')

# 4. Define o arquivo exato que o Streamlit está usando
# (Assim todo mundo olha para o MESMO arquivo)
DB_PATH = os.path.join(PASTA_BANCO, 'dados_user_Alan.db')


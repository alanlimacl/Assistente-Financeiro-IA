from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from app.config import BD_PASTA

BANCO = BD_PASTA / 'banco.db'

banco_base = create_engine(f"sqlite:///{BANCO}")

Base = declarative_base()

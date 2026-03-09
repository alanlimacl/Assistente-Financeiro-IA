from sqlalchemy import Column, String, Integer, Boolean, Numeric, ForeignKey
from app.roteador_api.conexao_bd import Base

class Usuario(Base):
    __tablename__ = 'usuario'
    
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String, nullable=False)
    email = Column('email', String, nullable=False)
    senha = Column('senha', String, nullable=False)
    ativo = Column('ativo', Boolean, default=True)
    
    # def __init__(self, nome, email, senha, ativo = True):
    #     self.nome = nome
    #     self.email = email
    #     self.senha = senha
    #     self.ativo = ativo
    

class Financas(Base):
    __tablename__ = 'financas'
    
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    valor = Column('valor', Numeric(10, 2), nullable=False)
    item = Column('item', String, nullable=False)
    categoria = Column('categoria', String, nullable=True)
    metodo_pagamento = Column('metodo_pagamento', String, nullable=False)
    data = Column('data', String, nullable=False)
    id_usuario = Column('id_usuario', ForeignKey('usuario.id'))
    
    def __init__(self, valor, item, categoria, metodo_pagamento, data, id_usuario):
        self.valor = valor
        self.item = item 
        self.categoria = categoria 
        self.metodo_pagamento = metodo_pagamento
        self.data = data 
        self.id_usuario = id_usuario
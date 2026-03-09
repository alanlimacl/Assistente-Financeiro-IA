from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError
import os

from app.roteador_api.modelos import Usuario
from app.roteador_api.conexao_bd import banco_base
from app.roteador_api.config import oauth2_esquema, SECRET_KEY, ALGORITHM


def pegar_sessao_bd():
    try:
        SESSION = sessionmaker(bind=banco_base)
        sessao = SESSION()
        yield sessao
    
    finally:
        sessao.close()


def checar_token(token: str = Depends(oauth2_esquema), sessao: Session = Depends(pegar_sessao_bd)):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM) # Retorna um dicionário com verificação do Token
        id_usuario = int(dict_info.get('sub')) # Pegando o ID do Usuário dentro do dicionário de acesso
        
    except JWTError: # Caso não tenha validado, retorna erro de token expirado ou acesso negado.
        raise HTTPException(status_code=401, detail='Acesso negado! Verifique o seu token de acesso.') 
    
    usuario = sessao.query(Usuario).filter(Usuario.id == id_usuario).first()
    
    if not usuario:
        raise HTTPException(status_code=401, detail='Acesso inválido!')
    
    return usuario




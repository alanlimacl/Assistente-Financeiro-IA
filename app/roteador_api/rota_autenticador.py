from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import bcrypt

from app.roteador_api.esquemas import UsuarioEsquema, LoginEsquema, RequisicaoRefreshTokenEsquema
from app.roteador_api.dependencias import pegar_sessao_bd
from app.roteador_api.config import ACESSO_TOKEN_MINUTOS_EXPIRAR, ALGORITHM, SECRET_KEY
from app.roteador_api.modelos import Usuario


autenticador_roteador = APIRouter(prefix='/autenticador', tags=['Autenticador'])


def obter_hash_senha(senha: str) -> str:
    # 1. Converte a senha de texto para bytes (exigência do bcrypt)
    senha_bytes = senha.encode('utf-8')
    
    # 2. Gera o salt aleatório e cria o hash
    salt = bcrypt.gensalt()
    hash_senha = bcrypt.hashpw(senha_bytes, salt)
    
    # 3. Converte de volta para string para salvar no banco de dados (VARCHAR)
    return hash_senha.decode('utf-8')


def autenticar_usuario(email, senha_digitada, sessao):
    usuario = sessao.query(Usuario).filter(Usuario.email == email).first()
    
    if not usuario:
        return False
    
    hash_banco_bytes = usuario.senha.encode('utf-8')
    senha_digitada_bytes = senha_digitada.encode('utf-8')
    
    senha_correta = bcrypt.checkpw(senha_digitada_bytes, hash_banco_bytes)
    
    if not senha_correta:
        return False
    
    return usuario


def criar_token(id_usuario, duracao_token = timedelta(minutes=ACESSO_TOKEN_MINUTOS_EXPIRAR), tipo_token='access'):
    
    data_expira = datetime.now(timezone.utc) + duracao_token
    dic_info = {'sub': str(id_usuario), 
                'exp': data_expira,
                'type': tipo_token}
    
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return encoded_jwt
    

@autenticador_roteador.post("/criar-conta")
async def criar_conta(usuario_esquema: UsuarioEsquema, sessao: Session = Depends(pegar_sessao_bd)):
    usuario_existente = sessao.query(Usuario).filter(Usuario.email == usuario_esquema.email).first()
    
    if usuario_existente:
        raise HTTPException(status_code=401, detail='Já existe um usuário com esse e-mail cadastrado. Por favor, use um e-mail diferente.')
    
    else:
        senha_criptografada = obter_hash_senha(usuario_esquema.senha)
        
        novo_usuario = Usuario(nome = usuario_esquema.nome,
                                email = usuario_esquema.email,
                                senha = senha_criptografada)
        sessao.add(novo_usuario)
        sessao.commit()
    
    return {'mensagem': f'Usuário "{usuario_esquema.nome}" registrado com sucesso!'}


@autenticador_roteador.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), sessao: Session = Depends(pegar_sessao_bd)):
    usuario = autenticar_usuario(form_data.username, form_data.password, sessao)
    
    if not usuario:
        raise HTTPException(status_code=401, detail= 'Não existe usuário cadastrado com esse email. Por favor, use um e-mail válido para login.')
    
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7), tipo_token='refresh') 

                
        return {'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'bearer',
                'nome': usuario.nome,
                'id': usuario.id}
        

@autenticador_roteador.post('/refresh-token')
async def renovar_refresh_token(requisicao: RequisicaoRefreshTokenEsquema):
    try:
        # 1. Tenta abrir a "chave mestra"
        payload = jwt.decode(requisicao.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        
        id_usuario: str = payload.get('sub')
        tipo_token: str = payload.get("type")

        # 2. Verifica se o token é mesmo de refresh e se tem um usuário
        if id_usuario is None or tipo_token != "refresh":
            raise HTTPException(status_code= 401, detail="Token de renovação inválido ou corrompido.")

        # 3. Se deu tudo certo, cria um NOVO access token de 30 minutos!
        novo_access_token = criar_token(id_usuario)

        return {
            "access_token": novo_access_token,
            "token_type": "bearer"
        }
        
    except JWTError:
        # Se o refresh token (de 7 dias) também expirou, aí sim o usuário é deslogado
        raise HTTPException(status_code=401, detail="Sua sessão expirou completamente. Faça login novamente.")
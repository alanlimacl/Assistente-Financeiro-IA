from pydantic import BaseModel
from typing import Optional

class UsuarioEsquema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    
    class Configuracao:
        from_attributes = True
        

class FinancasEsquema(BaseModel):
    valor: float
    item: str
    categoria: str
    metodo_pagamento: str 
    data: str
    
    class Configuracao:
        from_attributes = True


class MetaGastosEsquema(BaseModel):
    valor: float 
    categoria: str
    data_mes: str
    
    class Configuracao:
        from_attributes = True


class LoginEsquema(BaseModel):
    email: str
    senha: str
    
    class Configuracao:
        from_attributes = True
        

class RequisicaoRefreshTokenEsquema(BaseModel):
    refresh_token : str


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
from fastapi.security import OAuth2PasswordBearer
import os

ACESSO_TOKEN_MINUTOS_EXPIRAR = int(os.getenv("ACESSO_TOKEN_MINUTOS_EXPIRAR"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_esquema = OAuth2PasswordBearer(tokenUrl="/autenticador/login")

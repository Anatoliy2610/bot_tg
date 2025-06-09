from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer


load_dotenv()


SECRET_KEY_TOKEN = os.getenv('SECRET_KEY_TOKEN')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

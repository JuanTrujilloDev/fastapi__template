from cryptography.fernet import Fernet
from passlib.context import CryptContext

from fastapi__template.settings import settings

STRING_HASHER = CryptContext(schemes=["bcrypt"], deprecated="auto")
STRING_CIPHER = Fernet(settings.SECRET_KEY)

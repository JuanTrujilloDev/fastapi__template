from cryptography.fernet import Fernet

from fastapi__template.settings import settings

STRING_CIPHER = Fernet(settings.SECRET_KEY)

from config import *  # noqa
from cryptography.fernet import Fernet

# string to bytes
SECRET_KEY = bytes(SECRET_KEY, encoding="utf-8")
fernet = Fernet(SECRET_KEY)


def encrypt(message: str) -> str:
    return fernet.encrypt(bytes(message, encoding="utf-8")).decode("utf-8")


def decrypt(message: str) -> str:
    return fernet.decrypt(bytes(message, encoding="utf-8")).decode("utf-8")

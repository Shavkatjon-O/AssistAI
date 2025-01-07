from typing import Type

from config import *  # noqa
from database import get_db
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import JWTError, jwt
from models import Admin
from oauth2 import bearer_security
from schemas.admins import TokenData
from sqlalchemy.orm import Session


async def get_current_admin(
    token: HTTPAuthorizationCredentials = Depends(bearer_security),
    db: Session = Depends(get_db),
) -> Type[Admin]:
    exception = HTTPException(
        status_code=404,
        detail="Not found",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token=token.credentials,
            key=SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise exception
        token_data = TokenData(username=username)
    except JWTError:
        raise exception

    db_user = db.query(Admin).filter(Admin.username == token_data.username).first()

    if db_user is None:
        raise exception
    return db_user


def create_initial_admin():
    db: Session = next(get_db())
    admin = db.query(Admin).filter(Admin.username == "admin").first()
    if not admin:
        admin = Admin(username="admin")
    admin.set_password("admin")
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

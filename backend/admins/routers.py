from fastapi import APIRouter
import datetime

from database import get_db
from fastapi import Depends, HTTPException
from jwt import create_access_token, verify_password
from models import Admin
from sqlalchemy.orm import Session
from admins.schemas import Token, AdminCreate, AdminOut
from admins.utils import get_current_admin


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.post("/token", response_model=Token)
async def get_token(data: AdminCreate, db: Session = Depends(get_db)):
    db_user = db.query(Admin).filter(Admin.username == data.username).first()
    if not db_user or not verify_password(data.password, db_user.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=datetime.timedelta(hours=24),
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=AdminOut)
async def profile(current_admin: Admin = Depends(get_current_admin)):
    return current_admin

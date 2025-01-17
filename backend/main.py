import datetime

import uvicorn
from database import get_db
from fastapi import Depends, FastAPI, HTTPException
from jwt import create_access_token, get_hashed_password, verify_password
from models import User
from schemas.auth import Token, UserCreate, UserOut
from sqlalchemy.orm import Session
from utils.auth import get_current_user
from admins.utils import create_initial_admin
from fastapi.middleware.cors import CORSMiddleware

from admins.routers import router as admin_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_router)


@app.post("/sign-up", response_model=UserOut)
async def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered",
        )

    hashed_password = get_hashed_password(user.password)
    db_user = User(username=user.username, password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/sign-in", response_model=Token)
async def sign_in(data: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == data.username).first()
    if not db_user or not verify_password(data.password, db_user.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=datetime.timedelta(minutes=5),
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@app.get("/me", response_model=UserOut)
async def profile(current_user: User = Depends(get_current_user)):
    return current_user


if __name__ == "__main__":
    create_initial_admin()

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

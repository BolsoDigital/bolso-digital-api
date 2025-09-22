from fastapi import APIRouter, Depends, HTTPException
from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import Token, UserLogin
from app.schemas.user import UserCreate, UserOut
from app.utils.auth import create_access_token

router = APIRouter(tags=['Auth'])


@router.post('/register', response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail='Email já registrado')

    hashed_pw = bcrypt.hash(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        phone_number=user.phone_number,
        hashed_password=hashed_pw,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post('/login', response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not user.verify_password(data.password):
        raise HTTPException(status_code=401, detail='Credenciais inválidas')

    token = create_access_token(data={'sub': str(user.id)})
    return {'access_token': token, 'token_type': 'bearer'}
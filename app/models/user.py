from sqlalchemy import Column, Integer, String
from app.database import Base

class CustonUser(Base):
    __tablename__ = "custom_user"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    username = Column(String)
    email = Column(String)


def get_user_by_phone(db, phone_number: str):
    return db.query(CustonUser).filter(CustonUser.phone_number == phone_number).first()

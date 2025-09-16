from passlib.hash import bcrypt
from sqlalchemy import BigInteger, Boolean, Column, DateTime, String

from app.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String)
    cpf = Column(String, unique=True, index=True)
    phone_number = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    create_at = Column(DateTime)
    is_active = Column(Boolean, default=True)

    def verify_password(self, password: str):
        return bcrypt.verify(password, self.password)
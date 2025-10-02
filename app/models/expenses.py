from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)

from app.database import Base


class Expenses(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    value = Column(Numeric)
    id_category = Column(Integer, ForeignKey('category.id'))
    update_at = Column(DateTime)
    description = Column(Text)
    id_user = Column(BigInteger, ForeignKey('user.id'))
    payment_method = Column(String)
    is_recurring = Column(Boolean)

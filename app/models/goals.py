from sqlalchemy import BigInteger, Column, Date, ForeignKey, Integer, Numeric

from app.database import Base


class Goals(Base):
    __tablename__ = 'goals'

    id = Column(BigInteger, primary_key=True, index=True)
    id_user = Column(BigInteger, ForeignKey('custom_user.id'))
    id_category = Column(Integer, ForeignKey('category.id'))
    target_value = Column(Numeric)
    period_start = Column(Date)
    period_end = Column(Date)

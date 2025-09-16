from datetime import datetime

from pydantic import BaseModel


class ExpensesBase(BaseModel):
    value: float
    id_category: int
    description: str
    id_user: int
    payment_method: str
    is_recurring: bool


class ExpensesCreate(ExpensesBase):
    pass


class ExpensesOut(ExpensesBase):
    id: int
    update_at: datetime

    class Config:
        from_attributes = True
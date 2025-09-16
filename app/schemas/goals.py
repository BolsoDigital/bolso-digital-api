from datetime import date

from pydantic import BaseModel


class GoalsBase(BaseModel):
    id_user: int
    id_category: int
    target_value: float
    period_start: date
    period_end: date


class GoalsCreate(GoalsBase):
    pass


class GoalsOut(GoalsBase):
    id: int

    class Config:
        from_attributes = True
from app.models.expenses import Expense


class ExpenseRepository:
    def __init__(self, db):
        self.db = db

    def save(self, parsed_data, id_user):
        # Implemente aqui a lógica para persistir o gasto
        expense = Expense(**parsed_data, user_id=id_user)
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

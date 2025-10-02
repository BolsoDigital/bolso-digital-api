from app.services.expenses import save_expense


class ExpenseRepository:
    def __init__(self, db):
        self.db = db

    def save(self, structured_data, id_user):
        return save_expense(self.db, structured_data, id_user)

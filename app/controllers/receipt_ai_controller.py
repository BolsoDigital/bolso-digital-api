from app.use_cases.process_receipt import ProcessReceiptUseCase
from app.repositories.expense_repository import ExpenseRepository


class ReceiptAIController:
    def __init__(self, db):
        self.db = db

    async def process_receipt(self, file, id_user):
        use_case = ProcessReceiptUseCase(self.db)
        return await use_case.execute(file, id_user)
    
    def delete_payment(self, payment_id: int, id_user: int):
        repository = ExpenseRepository(self.db)
        return repository.delete(payment_id, id_user)    

from app.use_cases.process_receipt import ProcessReceiptUseCase


class ReceiptAIController:
    def __init__(self, db):
        self.db = db

    async def process_receipt(self, file, id_user):
        use_case = ProcessReceiptUseCase(self.db)
        return await use_case.execute(file, id_user)

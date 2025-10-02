from app.use_cases.analyze_expense import AnalyzeExpenseUseCase


class ExpensesAIController:
    def __init__(self, db):
        self.db = db

    async def analyze_expense(self, message, image, id_user):
        use_case = AnalyzeExpenseUseCase(self.db)
        return await use_case.execute(message, image, id_user)

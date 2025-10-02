from app.repositories.expense_repository import ExpenseRepository
from app.utils.expense_parser import (
    parse_expense_from_image,
    parse_expense_from_text,
)


class AnalyzeExpenseUseCase:
    def __init__(self, db):
        self.repository = ExpenseRepository(db)

    async def execute(self, message, image, id_user):
        parsed = None
        if message:
            parsed = parse_expense_from_text(message)
        elif image:
            parsed = await parse_expense_from_image(image)

        if not parsed:
            raise ValueError('Não foi possível interpretar o gasto.')

        expense = self.repository.save(parsed, id_user)
        return {'dados_extraidos': parsed, 'id_registro': expense.id}

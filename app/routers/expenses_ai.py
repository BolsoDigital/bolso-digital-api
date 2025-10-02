from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile

from app.utils.expense_parser import (
    parse_expense_from_image,
    parse_expense_from_text,
)

router = APIRouter(prefix='/ai', tags=['IA Despesas'])


@router.post('/analyze-expense/')
async def analyze_expense(
    message: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
):
    if not message and not image:
        return {'error': 'Envie uma mensagem de texto ou imagem.'}

    if message:
        parsed = parse_expense_from_text(message)
    elif image:
        parsed = await parse_expense_from_image(image)

    if not parsed:
        return {'error': 'Não foi possível interpretar o gasto.'}

    return parsed

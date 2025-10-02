from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.controllers.expenses_ai_controller import ExpensesAIController
from app.database import get_db

router = APIRouter(prefix='/ai', tags=['IA Despesas'])


@router.post('/analyze-expense/')
async def analyze_expense(
    message: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    id_user: int = 1,
):
    if not message and not image:
        raise HTTPException(
            status_code=400, detail='Envie uma mensagem de texto ou imagem.'
        )

    controller = ExpensesAIController(db)
    try:
        return await controller.analyze_expense(message, image, id_user)
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f'Erro ao analisar: {str(e)}'
        )

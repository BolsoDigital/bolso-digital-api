from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status, Query
from sqlalchemy.orm import Session

from app.controllers.receipt_ai_controller import ReceiptAIController
from app.database import get_db

from app.utils.expense_parser import (
    parse_expense_from_image,
    parse_expense_from_text,
)

router = APIRouter(prefix='/ai', tags=['IA Despesas'])


@router.post('/upload-payment/')
async def analyze_expense(
    message: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    id_user: int = Form(...),
):
    if not message and not image:
        raise HTTPException(
            status_code=400, detail='Envie uma mensagem de texto ou imagem.'
        )
        
    controller = ReceiptAIController(db)
    if message:
        try:
            parsed = parse_expense_from_text(message)
            if not parsed:
                raise ValueError('Não foi possível interpretar o gasto.')
            return parsed
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f'Erro ao analisar: {str(e)}'
            )
    elif image:
        try:
            return await controller.process_receipt(image, id_user)
        except ValueError as ve:
            raise HTTPException(status_code=422, detail=str(ve))
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f'Erro ao analisar: {str(e)}'
            )

@router.delete('/delete-payment/{payment_id}')
async def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    id_user: int = Query(...),
):
    controller = ReceiptAIController(db)
    try:
        deleted = controller.delete_payment(payment_id, id_user)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pagamento com id {payment_id} não encontrado."
            )
        return {"message": f"Pagamento {payment_id} deletado com sucesso."}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao deletar pagamento: {str(e)}"
        )
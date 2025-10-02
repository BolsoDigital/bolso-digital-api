from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Category, Expenses


class ExpenseRepository:
    def __init__(self, db):
        self.db = db

    def save(self, structured_data, id_user):
        return save_expense(self.db, structured_data, id_user)
    
    def delete(self, expense_id: int, user_id: int):
        expense = (
            self.db.query(Expenses)  # <-- aqui usa o model correto
            .filter_by(id=expense_id, id_user=user_id)
            .first()
        )
        if not expense:
            return False
        self.db.delete(expense)
        self.db.commit()
        return True    
    

def get_or_create_category(db: Session, name: str):
    categoria = db.query(Category).filter_by(name=name).first()
    if not categoria:
        categoria = Category(name=name)
        db.add(categoria)
        db.commit()
        db.refresh(categoria)
    return categoria


def save_expense(db: Session, dados: dict, id_user: int):
    try:
        update_at = datetime.strptime(
            f"{dados['data']} {dados['hora']}", '%d/%m/%Y %H:%M:%S'
        )
    except Exception:
        update_at = datetime.utcnow()

    categoria = get_or_create_category(db, dados.get('categoria', 'outros'))


    expense = Expenses(
        value=dados['valor'],
        id_category=categoria.id,
        update_at=update_at,
        description=f"Pagamento de {dados['pagador']['nome']} para {dados['destinatario']['nome']}",
        id_user=id_user,
        payment_method='Pix',
        is_recurring=False,
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense
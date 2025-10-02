from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Category, Expenses


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

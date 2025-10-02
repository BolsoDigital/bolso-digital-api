from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth, expenses_ai, receipt_ai

# Cria as tabelas no banco (temporário)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# # Inclui as rotas
# app.include_router(user.router)
# app.include_router(expenses.router)
# app.include_router(income.router)
# app.include_router(goals.router)
# app.include_router(category.router)
# app.include_router(auth.router)
app.include_router(expenses_ai.router)
app.include_router(receipt_ai.router)

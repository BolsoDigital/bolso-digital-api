import json
import os

import requests
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from app.repositories.expense_repository import ExpenseRepository
from app.utils import parse_expense_from_image

CATEGORIAS_VALIDAS = [
    'alimentação',
    'transporte',
    'aluguel',
    'serviços',
    'saúde',
    'educação',
    'lazer',
    'outros',
]


class ProcessReceiptUseCase:
    def __init__(self, db):
        self.repository = ExpenseRepository(db)

    def interpret_text_with_ai(self, text):
        prompt = PromptTemplate.from_template(
            """
            Analise o texto do documento financeiro abaixo.
            Ele pode ser um comprovante de Pix, TED, DOC, Compra no débito, Compra no crédito, ou um boleto bancário.
            Se algum dado não estiver presente no texto, deixe o campo vazio ("").
            Não invente valores.
            Texto do comprovante:
            {text}

            
            - A data pode aparecer junto com a hora (exemplo: "02/10/2025 - 21:40:58").
            - Nesse caso, separe a data em "02/10/2025" e a hora em "21:40:58".
            - Se tiver código de barras então é um boleto.
            Retorne em formato JSON com as seguintes chaves:
            - valor (float)
            - data (formato dd/mm/yyyy)
            - hora (formato HH:MM:SS)
            - destinatario (nome, CPF, banco)
            - pagador (nome, CPF, instituição)
            - categoria (escolha entre: alimentação, transporte, aluguel, serviços, saúde, educação, lazer, outros)
            - Tipo de transferencia: (Pix, Boleto, TED, DOC, Crédito, Débito ou outro)
            """
        )
        llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')
        chain = prompt | llm
        result = chain.invoke({'text': text})
        print("💬 Prompt enviado para o modelo:", {text})
        print("🔎 Saída do modelo:", result.content)
        try:
            dados = json.loads(result.content)
            categoria = dados.get('categoria', '').strip().lower()
            if categoria not in CATEGORIAS_VALIDAS:
                dados['categoria'] = 'outros'
            return dados
        except json.JSONDecodeError as e:
            raise ValueError(
                f'Erro ao converter resposta da IA para JSON: {e}'
            )

    async def execute(self, file, id_user):
        parsed_data = await parse_expense_from_image(file)
        if not parsed_data:
            raise ValueError('Texto não reconhecido na imagem')
        structured_data = self.interpret_text_with_ai(parsed_data.get("raw_text", ""))
        expense = self.repository.save(structured_data, id_user)
        return {'dados_extraidos': structured_data, 'id_registro': expense.id}

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
            Você é um extrator confiável de informações de comprovantes financeiros.
            O texto abaixo pode ser: Pix, TED, DOC, Débito, Crédito ou boleto.

             Regras importantes:
            - NÃO invente nada. Apenas extraia.
            - Se não houver um dado, deixe como "" (string vazia).
            - Remova símbolos estranhos e caracteres inválidos.
            - CPF/CNPJ devem conter apenas números.
            - "valor" deve ser float usando . como separador decimal.
            - Nunca retorne textos com caracteres como „ ’  ́ ~  — etc.

            Texto do comprovante:
            {text}

            Retorne APENAS JSON, no seguinte formato:

            {{
                "valor": float,
                "data": "dd/mm/yyyy",
                "hora": "HH:MM:SS",
                "destinatario": {{
                    "nome": "",
                    "CPF": "",
                    "banco": ""
                }},
                "pagador": {{
                    "nome": "",
                    "CPF": "",
                    "instituicao": ""
                }},
                "categoria": "alimentação | transporte | aluguel | serviços | saúde | educação | lazer | outros",
                "tipo_transferencia": "Pix | Boleto | TED | DOC | Crédito | Débito | Outro"
            }}

            Certifique-se que o JSON seja válido.
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

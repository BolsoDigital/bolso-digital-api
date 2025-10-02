import json
import os

import requests
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from app.repositories.expense_repository import ExpenseRepository

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

    def extract_text_from_image(self, file):
        API_KEY = os.getenv('OCR_SPACE_API_KEY')
        image_bytes = file.file.read()
        response = requests.post(
            'https://api.ocr.space/parse/image',
            files={'file': (file.filename, image_bytes)},
            data={'apikey': API_KEY, 'language': 'por'},
        )
        try:
            result = response.json()
            return result['ParsedResults'][0]['ParsedText']
        except (KeyError, IndexError):
            return ''

    def interpret_text_with_ai(self, text):
        prompt = PromptTemplate.from_template(
            """
Extraia as informações do texto do comprovante Pix abaixo.
Texto do comprovante:
{text}
Retorne em formato JSON com as seguintes chaves:
- valor (float)
- data (formato dd/mm/yyyy)
- hora (formato HH:MM:SS)
- destinatario (nome, CPF, banco)
- pagador (nome, CPF, instituição)
- categoria (escolha entre: alimentação, transporte, aluguel, serviços, saúde, educação, lazer, outros)
- Tipo de transferencia: (se for entre contas, para terceiros, DOC, TED, Pix)
"""
        )
        llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')
        chain = prompt | llm
        result = chain.invoke({'text': text})
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
        text = self.extract_text_from_image(file)
        if not text.strip():
            raise ValueError('Texto não reconhecido na imagem')
        structured_data = self.interpret_text_with_ai(text)
        expense = self.repository.save(structured_data, id_user)
        return {'dados_extraidos': structured_data, 'id_registro': expense.id}

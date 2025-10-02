import json

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

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


class AIService:
    def interpret_text(self, text):
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

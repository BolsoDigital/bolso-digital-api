# 💸 EcoApp - Gestão de Despesas Inteligente

O **EcoApp** é uma aplicação que permite aos usuários gerenciar despesas de forma inteligente a partir de **comprovantes de pagamento** (PIX, boletos, transferências, etc.).  

Através de **OCR + IA (LangChain + OpenAI)**, o sistema extrai automaticamente as informações do comprovante, interpreta os dados relevantes e classifica a despesa em categorias predefinidas.  

Além disso, os dados são armazenados em um **banco de dados relacional (SQLite/SQLAlchemy)** para que cada usuário possa acompanhar seus gastos ao longo do tempo.

---

## 🚀 Funcionalidades

- Upload de comprovantes em imagem (`.jpg`, `.png`).
- Extração de texto via **OCR.Space API**.
- Interpretação automática dos dados via **LangChain + OpenAI**.
- Estruturação em JSON com:
  - Valor da transação  
  - Data e hora  
  - Pagador (nome, CPF, instituição)  
  - Destinatário (nome, CPF, banco)  
  - Categoria da despesa (alimentação, transporte, aluguel, serviços, saúde, educação, lazer, outros)
- Classificação automática da despesa em categorias válidas.
- Armazenamento dos dados no banco de dados (`expenses`, `category`, `user`).
- API REST desenvolvida em **FastAPI**, pronta para integração com apps e chatbots.
- Integração futura com **WhatsApp (Evolution API)** para envio de comprovantes diretamente pelo app de mensagens.

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.11+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://www.langchain.com/) + [OpenAI API](https://platform.openai.com/)
- [OCR.Space API](https://ocr.space/OCRAPI)
- [SQLAlchemy](https://www.sqlalchemy.org/) + SQLite (ou PostgreSQL futuramente)
- [Uvicorn](https://www.uvicorn.org/)

---

## 📂 Estrutura do Projeto
EcoApp/
│── app/
│ ├── main.py # Inicialização da API
│ ├── database.py # Conexão com banco de dados
│ ├── models/ # Definição das tabelas (Expenses, Category, User)
│ ├── routers/
│ │ ├── receipt_ai.py # Rota para upload e interpretação de comprovantes
│ │ └── auth.py # (futuro) Autenticação de usuários
│ └── utils/ # Funções auxiliares (ex: OCR, parse de dados)
│
│── .env # Chaves de API e configs locais
│── requirements.txt # Dependências do projeto
│── README.md # Documentação do projeto


---

## ⚙️ Instalação e Configuração

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/ecoapp.git
   cd ecoapp


2. Crie um ambiente virtual e ative:

  ```bash
  python -m venv venv
  source venv/bin/activate   # Linux/Mac
  venv\Scripts\activate      # Windows
  ````


3. Instale as dependências:
  ```bash
  pip install -r requirements.txt
  ````

4. Configure o arquivo .env:

```bash
  OCR_SPACE_API_KEY=suachaveaqui
  OPENAI_API_KEY=suachaveaqui
  DATABASE_URL=sqlite:///./eco.db
````

Crie o banco de dados:

from app.database import Base, engine
Base.metadata.create_all(bind=engine)


Rode a API:

uvicorn app.main:app --reload

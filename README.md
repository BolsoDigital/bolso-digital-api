# 💸 Bolso Digital - Gestão de Despesas Inteligente

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-0eb7ad?logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-0.3.27-4E7DD9?logo=langchain)
![License](https://img.shields.io/github/license/BolsoDigital/bolso-digital-api)

## 📑 Sumário

- [Descrição](#descrição)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Configuração](#instalação-e-configuração)
- [Exemplos de Uso da API](#exemplos-de-uso-da-api)
- [Licença](#licença)
- [Links Úteis](#links-úteis)

---

## 📝 Descrição

O **EcoApp** é uma aplicação que permite aos usuários gerenciar despesas de forma inteligente a partir de **comprovantes de pagamento** (PIX, boletos, transferências, etc.).

Através de **OCR + IA (LangChain + OpenAI)**, o sistema extrai automaticamente as informações do comprovante, interpreta os dados relevantes e classifica a despesa em categorias predefinidas.

Além disso, os dados são armazenados em um **banco de dados relacional (SQLite/SQLAlchemy)** para que cada usuário possa acompanhar seus gastos ao longo do tempo.

---

## 🚀 Funcionalidades

- Upload de comprovantes em imagem (`.jpg`, `.png`)
- Extração de texto via **OCR.Space API**
- Interpretação automática dos dados via **LangChain + OpenAI**
- Estruturação em JSON com:
  - Valor da transação
  - Data e hora
  - Pagador (nome, CPF, instituição)
  - Destinatário (nome, CPF, banco)
  - Categoria da despesa (alimentação, transporte, aluguel, serviços, saúde, educação, lazer, outros)
- Classificação automática da despesa em categorias válidas
- Armazenamento dos dados no banco de dados (`expenses`, `category`, `user`)
- API REST desenvolvida em **FastAPI**, pronta para integração com apps e chatbots
- Integração futura com **WhatsApp (Evolution API)** para envio de comprovantes diretamente pelo app de mensagens

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.11+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://www.langchain.com/) + [OpenAI API](https://platform.openai.com/)
- [OCR.Space API](https://ocr.space/OCRAPI)
- [SQLAlchemy](https://www.sqlalchemy.org/) + SQLite (ou PostgreSQL futuramente)
- [Uvicorn](https://www.uvicorn.org/)

---

## 📋 Pré-requisitos

- Python 3.11+
- Git

---

## ⚙️ Instalação e Configuração

1. Clone o repositório:
    ```bash
    git clone https://github.com/BolsoDigital/bolso-digital-api.git
    cd bolso-digital-api
    ```

2. Crie um ambiente virtual e ative:

    ```bash
    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    # ou
    venv\Scripts\activate      # Windows
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure o arquivo `.env`:

    ```env
    OCR_SPACE_API_KEY=suachaveaqui
    OPENAI_API_KEY=suachaveaqui
    DATABASE_URL=sqlite:///./eco.db
    ```

5. Crie o banco de dados:
    ```python
    from app.database import Base, engine
    Base.metadata.create_all(bind=engine)
    ```

6. Rode a API:
    ```bash
    uvicorn app.main:app --reload
    ```

---

## 📦 Exemplos de Uso da API

Após iniciar o servidor, acesse a documentação interativa em: [http://localhost:8000/docs](http://localhost:8000/docs)

Exemplo de upload via `curl`:
```bash
curl -X POST "http://localhost:8000/upload" -F "file=@comprovante.png"
```

---

## 📄 Licença


---

## 🔗 Links Úteis

- [Reportar um bug](https://github.com/BolsoDigital/bolso-digital-api/issues)
- [Solicitar nova funcionalidade](https://github.com/BolsoDigital/bolso-digital-api/pulls)

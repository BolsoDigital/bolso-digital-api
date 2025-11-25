from fastapi import APIRouter, Request, Depends
import httpx
import os
import json

from app.database import get_db
from app.models.user import get_user_by_phone
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


@router.post("/webhook/whatsapp")
async def receive_message(request: Request, db=Depends(get_db)):
    data = await request.json()

    # 1. LOG DE DEPURAÇÃO: Ver o que o WhatsApp realmente mandou
    # print(f"Payload recebido: {json.dumps(data, indent=2)}")

    # 2. Extração Segura: Verifica se é realmente uma mensagem
    try:
        entry = data.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        
        # O WhatsApp manda status (lido/entregue) no mesmo webhook.
        # Se não tiver "messages", ignoramos sem ser erro.
        if "messages" not in value:
            # print("Evento de status ignorado (não é mensagem).")
            return {"status": "ignored_status_update"}
            
        message = value["messages"][0]
        
    except Exception as e:
        print(f"Erro ao extrair dados do JSON: {e}")
        return {"status": "ignored_structure_error"}

# 1. Pega o número que o WhatsApp mandou (Ex: "554591313371")
    sender = message["from"] 
    print(f"👤 Sender recebido do WhatsApp: {sender}")

    # 2. Normalização para o formato do seu banco (DDD + 9 Dígitos)
    phone_to_search = sender

    # Lógica: Se começa com 55 (Brasil) e tem 12 dígitos (55 + DDD + 8 números)
    # Significa que o WhatsApp "comeu" o 9º dígito.
    if sender.startswith("55") and len(sender) == 12:
        ddd = sender[2:4]       # Pega o DDD (ex: 45)
        number = sender[4:]     # Pega o resto (ex: 91313371)
        
        # Reconstrói no formato que está no seu banco: "45991313371"
        phone_to_search = f"{ddd}9{number}"
        
        print(f"🔧 Ajustando número Brasil: {sender} -> {phone_to_search}")

    # 3. Agora busca no banco usando o número formatado
    user = get_user_by_phone(db, phone_to_search)

    # Fallback: Se não achar, tenta buscar pelo sender original (vai que alguém cadastrou errado)
    if not user:
        print(f"⚠️ Não achei {phone_to_search}, tentando o original {sender}...")
        user = get_user_by_phone(db, sender)

    if not user:
        print(f"❌ Usuário {phone_to_search} não encontrado no banco.")
        await send_message(sender, "❗ Seu número não está cadastrado no sistema.")
        return {"status": "user_not_found"}

    user_id = user.id
    print(f"🔥 Usuário encontrado: ID={user_id}, Phone={user.phone_number}")

    # Lógica de TEXTO
    if message["type"] == "text":
        user_text = message["text"]["body"]
        print(f"💬 Texto recebido: {user_text}")
        await send_message(sender, f"Recebi sua mensagem:\n{user_text}")
        return {"status": "ok"}

    # Lógica de IMAGEM
    if message["type"] == "image":
        # print(" Imagem detectada! Iniciando download...")
        media_id = message["image"]["id"]
        WEB_TOKEN = os.getenv('WHATSAPP_TOKEN')

        async with httpx.AsyncClient() as client:
            # Passo 1: Pegar URL
            media_info = await client.get(
                f"https://graph.facebook.com/v18.0/{media_id}?fields=url",
                headers={"Authorization": f"Bearer {WEB_TOKEN}"}
            )
            
            if media_info.status_code != 200:
                # print(f" Erro ao pegar URL da mídia: {media_info.text}")
                return {"status": "error_getting_media_url"}

            media_json = media_info.json()
            url = media_json.get("url")

            if not url:
                # print(" URL não encontrada no JSON da mídia.")
                return {"status": "missing_media_url"}

            # Passo 2: Baixar Binário
            # print(f"⬇ Baixando imagem da URL: {url}")
            image_response = await client.get(
                url,
                headers={"Authorization": f"Bearer {WEB_TOKEN}"}
            )

            if image_response.status_code != 200:
                # print(f"Falha ao baixar imagem: {image_response.status_code}")
                return {"status": "download_failed"}
            
            image_bytes = image_response.content

        # Passo 3: Enviar para API AI
        # print("Enviando imagem para API de processamento...")
        async with httpx.AsyncClient(timeout=30.0) as client:
            files = {
                "image": ("comprovante.jpg", image_bytes, "image/jpeg")
            }
            data_payload = {"id_user": str(user_id)}

            try:
                process = await client.post(
                    "https://kisha-cotyledonoid-monistically.ngrok-free.dev/ai/upload-payment/",
                    files=files,
                    data=data_payload
                )
                
                # print(f" Resposta da API AI: {process.status_code}")
                
                if "application/json" in process.headers.get("content-type", ""):
                    result = process.json()
                else:
                    # print("Resposta não-JSON da API:", process.text)
                    result = {"msg": "Processado, mas sem JSON de retorno"}

            except Exception as e:
                # print(f" Erro ao conectar na API AI: {e}")
                await send_message(sender, "Ocorreu um erro interno ao processar sua imagem.")
                return {"status": "api_ai_error"}

        await send_message(sender, f"Análise concluída:\n{result}")

    return {"status": "ok"}


async def send_message(phone_number, text):
    WEB_TOKEN = os.getenv('WHATSAPP_TOKEN')
    PHONE_ID = os.getenv('PHONE_NUMBER_ID')

    url = f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": text}
    }

    async with httpx.AsyncClient() as client:
        await client.post(
            url,
            headers={"Authorization": f"Bearer {WEB_TOKEN}"},
            json=payload
        )

from fastapi import APIRouter, Request, Depends
import httpx
import os

from app.database import get_db
from app.models.user import get_user_by_phone
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


@router.get("/webhook/whatsapp")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == os.getenv('VERIFY_TOKEN'):
        return int(challenge)

    return {"error": "Token inválido"}


@router.post("/webhook/whatsapp")
async def receive_message(request: Request, db=Depends(get_db)):
    data = await request.json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
    except:
        return {"status": "ignored"}

    # Número do WhatsApp que enviou a mensagem
    sender = message["from"]  # Ex: "551199887766"

    # Procura no banco Django (tabela custom_user)
    user = get_user_by_phone(db, sender)

    if not user:
        await send_message(sender, "❗ Seu número não está cadastrado no sistema.")
        return {"status": "user_not_found"}

    user_id = user.id
    print(f"🔥 Usuário encontrado: ID={user_id}, Phone={user.phone_number}")


    if message["type"] == "text":
        user_text = message["text"]["body"]
        await send_message(sender, f"Recebi sua mensagem:\n{user_text}")
        return {"status": "ok"}


    if message["type"] == "image":
        media_id = message["image"]["id"]
        WEB_TOKEN = os.getenv('WHATSAPP_TOKEN')

        async with httpx.AsyncClient() as client:
            media_info = await client.get(
                f"https://graph.facebook.com/v18.0/{media_id}?fields=url",
                headers={"Authorization": f"Bearer {WEB_TOKEN}"}
            )

            media_json = media_info.json()

            if "url" not in media_json:
                print("ERRO: resposta do WhatsApp:", media_json)
                return {"status": "missing_media_url"}

            url = media_json["url"]

            image_bytes = await client.get(
                url,
                headers={"Authorization": f"Bearer {WEB_TOKEN}"}
            )

        # Agora enviamos o ID REAL do usuário para sua API
        async with httpx.AsyncClient() as client:
            files = {
                "image": ("comprovante.jpg", image_bytes.content, "image/jpeg")
            }

            data = {"id_user": str(user_id)}

            process = await client.post(
                "https://kisha-cotyledonoid-monistically.ngrok-free.dev/ai/upload-payment/",
                files=files,
                data=data
            )

            if "application/json" in process.headers.get("content-type", ""):
                result = process.json()
            else:
                print("\n\n===== ERRO NO PROCESSAMENTO DO COMPROVANTE =====")
                print("Status:", process.status_code)
                print("Response:", process.text)
                print("===============================================\n\n")
                result = {"error": "Resposta não JSON da API de análise"}

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

from fastapi import APIRouter, Request
import httpx
import json

router = APIRouter()

VERIFY_TOKEN = ""
WHATSAPP_TOKEN = ""
PHONE_NUMBER_ID = "" 


@router.get("/webhook/whatsapp")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)

    return {"error": "Token inválido"}


@router.post("/webhook/whatsapp")
async def receive_message(request: Request):
    data = await request.json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
    except:
        return {"status": "ignored"}

    sender = message["from"]

    # Se for texto
    if message["type"] == "text":
        user_text = message["text"]["body"]
        await send_message(sender, f"Recebi sua mensagem:\n{user_text}")
        return {"status": "ok"}

    # Se for imagem
    if message["type"] == "image":
        media_id = message["image"]["id"]

        async with httpx.AsyncClient() as client:
            media_info = await client.get(
                f"https://graph.facebook.com/v18.0/{media_id}?fields=url",
                headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
            )

            media_json = media_info.json()

            if "url" not in media_json:
                print("ERRO: resposta do WhatsApp:", media_json)
                return {"status": "missing_media_url"}

            url = media_json["url"]

            image_bytes = await client.get(
                url,
                headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
            )

        async with httpx.AsyncClient() as client:
            files = {
                "image": ("comprovante.jpg", image_bytes.content, "image/jpeg")
            }
            data = {"id_user": "1"}

            process = await client.post(
                "https://a4606a1a2424.ngrok-free.app/ai/upload-payment/",
                files=files,
                data=data
            )

        result = process.json()

        await send_message(sender, f"Análise concluída:\n{result}")

    return {"status": "ok"}


async def send_message(phone_number, text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": { "body": text }
    }

    async with httpx.AsyncClient() as client:
        await client.post(
            url,
            headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"},
            json=payload
        )

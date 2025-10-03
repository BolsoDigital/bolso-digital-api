import os
import re

import httpx
from dotenv import load_dotenv

load_dotenv()


def parse_expense_from_text(text: str):
    text = text.lower()
    match = re.search(
        r'(\d+(?:[\.,]\d{1,2})?)\s*(reais|r\$)?\s*(em|no|na)?\s*([\w\s]+)',
        text,
    )
    if match:
        valor = float(match.group(1).replace(',', '.'))
        categoria = match.group(4).strip()
        return {'valor': valor, 'categoria': categoria}
    return None


async def parse_expense_from_image(image_file):
    API_KEY = os.getenv('OCR_SPACE_API_KEY')
    if not API_KEY:
        raise ValueError("OCR_SPACE_API_KEY não definido no ambiente")
        
    url = 'https://api.ocr.space/parse/image'
    files = {'file': (image_file.filename, await image_file.read(), image_file.content_type)}
    data = {
        'apikey': API_KEY,
        'language': 'por',
        'isOverlayRequired': False,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data, files=files)

    try:
        result = response.json()
        if result.get('IsErroredOnProcessing'):
            return None
            
        parsed_results = result.get('ParsedResults')
        if not parsed_results:
            return None

        text = parsed_results[0].get('ParsedText', '')
        
        return {
            "raw_text": text,
            "parsed": parse_expense_from_text(text)
        }

    except Exception as e:
        print(f'[Erro OCR] {e}')
        return None

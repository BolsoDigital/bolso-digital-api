import os

import requests


class OCRService:
    def extract_text(self, file):
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

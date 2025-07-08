import httpx
from transformers import pipeline

from app.config import Config
from app.utils.logger import logger

HF_API_URL = "https://huggingface.co/GraphWiz/Mistral-7B"
HEADERS = {"Authorization": f"Bearer {Config.HUGGINGFACE_API_KEY}"}


async def analyze_sentiment(text: str) -> str:
    """Анализ тональности с использованием локальной модели"""
    try:
        if not hasattr(analyze_sentiment, "model"):
            analyze_sentiment.model = pipeline(
                "sentiment-analysis",
                model="blanchefort/rubert-base-cased-sentiment"
            )

        result = analyze_sentiment.model(text)[0]
        label = result['label'].lower()

        mapping = {
            'positive': 'positive',
            'negative': 'negative',
            'neutral': 'neutral'
        }
        return mapping.get(label, "unknown")
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {str(e)}")
        return "unknown"


async def query_mistral(payload: dict) -> dict:
    """Запрос к Mistral-7B через Hugging Face API"""
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            HF_API_URL,
            headers=HEADERS,
            json=payload
        )
        response.raise_for_status()
        return response.json()


async def categorize_complaint(text: str) -> str:
    prompt = f"""
    ### Задача:
    Определи категорию жалобы из следующих вариантов: техническая, оплата, другое.

    ### Жалоба:
    "{text}"

    ### Инструкции:
    1. Ответь только одним словом: "техническая", "оплата" или "другое".
    2. Не добавляй пояснений или дополнительного текста.

    ### Ответ:
    """

    try:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 10,
                "temperature": 0.1,
                "return_full_text": False
            }
        }

        response = await query_mistral(payload)

        generated_text = response[0]['generated_text'].strip().lower()

        for category in ["техническая", "оплата"]:
            if category in generated_text:
                return category

        return "другое"
    except httpx.HTTPStatusError as e:
        logger.error(f"Mistral API error: {e.response.status_code} - {e.response.text}")
        return "другое"
    except Exception as e:
        logger.error(f"Mistral request failed: {str(e)}")
        return "другое"


async def get_location_by_ip(query: str) -> dict:
    """Получение информации о местоположении по IP"""
    try:
        # Пропускаем локальные и приватные IP
        if query in ("127.0.0.1", "::1") or query.startswith(("10.", "192.168.", "172.")):
            return {}

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"http://ip-api.com/json/{query}",
                params={"fields": "country,regionName,city,lat,lon,isp"}
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"IP location lookup failed: {str(e)}")
        return {}

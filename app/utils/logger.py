import logging

from click import prompt
from sqlalchemy import text
from sqlalchemy.engine import result
from unicodedata import category

logger = logging.getLogger("complaint_api")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.debug(f"Sending to sentiment API: {text}")
# После получения ответа
logger.debug(f"Received sentiment: {result}")

# В функции categorize_complaint
logger.debug(f"Sending to OpenAI: {prompt}")
# После получения ответа
logger.debug(f"Received category: {category}")
import os
from dotenv import load_dotenv


load_dotenv()

class Settings:
    API_TITLE: str = os.getenv("API_TITLE", "dalia-cakes-api")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")
    INSTAGRAM_ACCESS_TOKEN: str = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")

    # Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # Business context (chatbot)
    BUSINESS_NAME: str = os.getenv("BUSINESS_NAME", "Dalia Bolos e Doces")
    BUSINESS_PHONE: str = os.getenv("BUSINESS_PHONE", "")
    BUSINESS_ADDRESS: str = os.getenv("BUSINESS_ADDRESS", "")
    BUSINESS_CITY: str = os.getenv("BUSINESS_CITY", "")
    BUSINESS_HOURS: str = os.getenv("BUSINESS_HOURS", "")
    BUSINESS_PAYMENT_METHODS: str = os.getenv("BUSINESS_PAYMENT_METHODS", "")
    BUSINESS_IFOOD_LINK: str = os.getenv("BUSINESS_IFOOD_LINK", "")
    BUSINESS_RECIPES_URL: str = os.getenv("BUSINESS_RECIPES_URL", "")
    BUSINESS_CAKE_PRICE_PER_KG: str = os.getenv("BUSINESS_CAKE_PRICE_PER_KG", "")
    BUSINESS_ORDER_ADVANCE_DAYS: str = os.getenv("BUSINESS_ORDER_ADVANCE_DAYS", "3 dias")
    CHATBOT_MAX_HISTORY: int = int(os.getenv("CHATBOT_MAX_HISTORY", "10"))

settings = Settings()

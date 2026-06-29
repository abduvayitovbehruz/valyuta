import requests
import logging

logger = logging.getLogger(__name__)

def get_exchange_rates():
    """Markaziy bank API'sidan USD, EUR va RUB kurslarini oladi."""
    url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
    
    try:

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        rates = {}

        target_codes = ["USD", "EUR", "RUB"]
        
        for item in data:
            ccy = item.get("Ccy")
            if ccy in target_codes:
                rates[ccy] = {
                    "name": item.get("CcyNm_UZ"),  
                    "rate": item.get("Rate"),      
                    "diff": item.get("Diff"),      
                    "date": item.get("Date")       
                }
                
        return rates
    except Exception as e:
        logger.error(f"Markaziy bank API'sidan ma'lumot olishda xato: {e}")
        return None
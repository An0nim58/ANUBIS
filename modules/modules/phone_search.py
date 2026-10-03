# modules/phone_search.py
import httpx
import phonenumbers
from phonenumbers import geocoder, carrier

class PhoneScanner:
    def __init__(self, phone: str):
        self.phone = phone
        self.clean_phone = self._clean_number()

    def _clean_number(self) -> str:
        """Очищает номер от лишних символов, приводя к формату +79991112233"""
        cleaned = "".join(filter(str.isdigit, self.phone))
        if cleaned.startswith("8") and len(cleaned) == 11:
            cleaned = "7" + cleaned[1:]
        if not cleaned.startswith("+") and cleaned:
            cleaned = "+" + cleaned
        return cleaned

    async def scan(self) -> dict:
        """Главный метод сбора информации по номеру телефона"""
        results = {
            "valid": False,
            "country": "Не определено",
            "operator": "Не определено",
            "whatsapp": "Не проверено",
            "links": []
        }

        try:
            parsed_number = phonenumbers.parse(self.clean_phone, None)
            if phonenumbers.is_valid_number(parsed_number):
                results["valid"] = True
                results["country"] = geocoder.description_for_number(parsed_number, "ru")
                results["operator"] = carrier.name_for_number(parsed_number, "ru")
        except Exception:
            return results

        if results["valid"]:
            # Проверяем WhatsApp через быстрый публичный запрос
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    wa_url = f"https://whatsapp.com{self.clean_phone.replace('+', '')}"
                    response = await client.get(wa_url)
                    if response.status_code == 200 and "shared_implicit_link" in response.text:
                        results["whatsapp"] = "Активен (Найден профиль)"
                    else:
                        results["whatsapp"] = "Не найден или скрыт"
            except Exception:
                results["whatsapp"] = "Ошибка проверки"

            # Генерируем полезные OSINT-ссылки
            raw_digits = self.clean_phone.replace("+", "")
            results["links"] = [
                f"https://whatsapp.com{raw_digits} (Написать в WA)",
                f"https://t.me{self.clean_phone} (Поиск ссылки в Telegram)",
                f"https://google.com{self.clean_phone}%22+OR+%22{raw_digits}%22 (Поиск совпадений в Google)"
            ]

        return results

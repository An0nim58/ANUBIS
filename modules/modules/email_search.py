# modules/email_search.py
import re
import dns.resolver


class EmailScanner:
    def __init__(self, email: str):
        self.email = email.strip().lower()

    def validate_email(self) -> bool:
        """Проверяет, соответствует ли строка базовому формату email"""
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(pattern, self.email))

    def check_mx_records(self) -> str:
        """Проверяет существование почтового сервера (MX-записей) для домена"""
        try:
            domain = self.email.split('@')[1]
            # Запрашиваем MX-записи у DNS
            answers = dns.resolver.resolve(domain, 'MX')
            if answers:
                return "Сервер активен (Принимает почту)"
        except Exception:
            return "Сервер не отвечает или не существует"
        return "Неизвестно"

    async def scan(self) -> dict:
        """Главный метод сбора информации по Email"""
        is_valid = self.validate_email()

        results = {
            "valid": is_valid,
            "mx_status": "Не проверено",
            "links": []
        }

        if is_valid:
            # Проверяем DNS-записи почты
            results["mx_status"] = self.check_mx_records()

            # Экранируем email для использования в поисковых URL
            query_email = self.email.replace("@", "%40")

            # Генерируем мощные OSINT-ссылки для поиска утечек и аккаунтов
            results["links"] = [
                f"https://leakcheck.io{self.email} (Проверка по базам утечек паролей LeakCheck)",
                f"https://intelx.io{self.email} (Глубокий поиск по архивам утечек Intelligence X)",
                f"https://google.com{self.email}%22 (Поиск точных упоминаний email в Google)",
                f"https://github.com{self.email}%22&type=code (Поиск email в коде на GitHub — часто находит приватные скрипты целей)",
                f"https://live.com (Форма восстановления Microsoft — введите email, чтобы увидеть часть привязанного телефона)"
            ]

        return results

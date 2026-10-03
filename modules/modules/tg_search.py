# modules/tg_search.py
import re


class TelegramScanner:
    def __init__(self, target: str):
        # Очищаем ввод от лишних пробелов, символов @ и ссылок типа t.me/
        self.target = target.strip().replace("@", "")
        if "t.me/" in self.target:
            self.target = self.target.split("t.me/")[-1]

    def analyze_input(self) -> tuple:
        """Определяет тип данных: цифровой ID или Username"""
        if self.target.isdigit():
            return "ID", self.target
        # Проверка валидности юзернейма Telegram (от 5 до 32 символов, буквы, цифры, подчёркивание)
        if re.match(r"^[a-zA-Z0-9_]{5,32}$", self.target):
            return "Username", self.target
        return "Invalid", self.target

    async def scan(self) -> dict:
        """Главный метод генерации OSINT-данных по Telegram"""
        input_type, clean_target = self.analyze_input()

        results = {
            "type": input_type,
            "target": clean_target,
            "links": []
        }

        if input_type == "Username":
            # OSINT по Юзернейму
            results["links"] = [
                f"https://t.me{clean_target} (Прямая ссылка на профиль цели)",
                f"https://tgstat.ru@{clean_target} (Поиск упоминаний администрируемых каналов на TGStat)",
                f"https://google.com{clean_target}%22 (Поиск точных упоминаний никнейма во всем вебе)",
                f"https://yandex.ru{clean_target}%22 (Поиск следов юзернейма в рунете)",
                f"https://marginalia.nu{clean_target} (Поиск по редким хакерским и приватным форумам)"
            ]
        elif input_type == "ID":
            # OSINT по Telegram ID
            results["links"] = [
                f"https://t.mec/{clean_target}/1 (Попытка генерации ссылки на внутренние сообщения)",
                f"https://google.com{clean_target}%22 (Поиск Telegram ID в слитых логах и текстовых базах в Google)",
                f"Примечание: Для деанона ID рекомендуется скопировать '{clean_target}' и отправить в боты-архивы (Глаз Бога, QuickOSINT) для поиска старых привязанных номеров."
            ]

        return results

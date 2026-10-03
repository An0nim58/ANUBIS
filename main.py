# main.py
import asyncio
import os
import sys
from rich.console import Console
from rich.panel import Panel

console = Console()

# Логотип горит плотным кроваво-красным цветом [#8B0000]
ANUBIS_ART = (
    "[bold #8B0000] █████╗ ███╗   ██╗██╗   ██╗██████╗ ██╗███████╗[/bold #8B0000]\n"
    "[bold #8B0000]██╔══██╗████╗  ██║██║   ██║██╔══██╗██║██╔════╝[/bold #8B0000]\n"
    "[bold #8B0000]███████║██╔██╗ ██║██║   ██║██████╔╝██║███████╗[/bold #8B0000]\n"
    "[bold #8B0000]██╔══██║██║╚██╗██║██║   ██║██╔══██╗██║╚════██║[/bold #8B0000]\n"
    "[bold #8B0000]██║  ██║██║ ╚████║╚██████╔╝██████╔╝██║███████║[/bold #8B0000]\n"
    "[bold #8B0000]╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚═╝╚══════╝[/bold #8B0000]\n"
)


async def main():
    while True:
        # Системная очистка терминала Windows / Linux
        os.system('cls' if os.name == 'nt' else 'clear')

        console.print(ANUBIS_ART)
        console.print("[bold #8B0000]─── [ Weighing the Digital Soul ] ────────────────────────[/bold #8B0000]\n")

        # Тексты меню горят истинным кровавым цветом
        console.print("[bold #8B0000]🩸 ГЛАВНОЕ МЕНЮ АНУБИСА:[/bold #8B0000]")
        console.print("[bold #8B0000]  1 — Мануалы (OSINT / Анонимность)[/bold #8B0000]")
        console.print("[bold #8B0000]  2 — Поиск по НОМЕРУ ТЕЛЕФОНА[/bold #8B0000]")
        console.print("[bold #8B0000]  3 — Поиск по ГОСНОМЕРУ АВТО[/bold #8B0000]")
        console.print("[bold #8B0000]  4 — Поиск по EMAIL[/bold #8B0000]")
        console.print("[bold #8B0000]  5 — Поиск по TELEGRAM (ID/Username)[/bold #8B0000]")
        console.print("[bold #8B0000]  0 — Выход из утилиты[/bold #8B0000]\n")

        choice = input("Выберите пункт меню: ").strip()
        print("\n")

        # 1. МАНУАЛЫ
        if choice == "1":
            console.print("[bold #8B0000]📚 ДОСТУПНЫЕ ВКЛАДКИ ЗНАНИЙ:[/bold #8B0000]")
            console.print("[bold #8B0000]  1 — Мануал по OSINT[/bold #8B0000]")
            console.print("[bold #8B0000]  2 — Мануал по анонимности[/bold #8B0000]")
            sub_choice = input("Пункт: ").strip()
            print("\n")
            from modules.manuals import show_osint_manual, show_anon_manual
            if sub_choice == "1":
                show_osint_manual()
            elif sub_choice == "2":
                show_anon_manual()
            else:
                console.print("[bold #8B0000][-] Неверный выбор.[/bold #8B0000]")
            input("\nНажмите Enter, чтобы вернуться в меню...")

        # 2. ПОИСК ПО ТЕЛЕФОНУ
        elif choice == "2":
            target = input("Введите номер телефона (например, +79991112233): ").strip()
            if target:
                from modules.phone_search import PhoneScanner
                with console.status("[bold #8B0000][*] Анубис взвешивает цифровой след телефона...", spinner="dots",
                                    spinner_style="bold #8B0000"):
                    scanner = PhoneScanner(target)
                    data = await scanner.scan()

                if data["valid"]:
                    links_str = "\n".join([f"[bold #8B0000]► {link}[/bold #8B0000]" for link in data["links"]])
                    console.print(Panel(
                        f"[bold #8B0000]Цель: {target}[/bold #8B0000]\n"
                        f"[bold #8B0000]Формат: {scanner.clean_phone}[/bold #8B0000]\n\n"
                        f"[bold #8B0000]▪ Страна/Регион: {data['country']}[/bold #8B0000]\n"
                        f"[bold #8B0000]▪ Оператор: {data['operator']}[/bold #8B0000]\n"
                        f"[bold #8B0000]▪ Статус WhatsApp: {data['whatsapp']}[/bold #8B0000]\n\n"
                        f"[bold #8B0000]Полезные OSINT-ссылки:[/bold #8B0000]\n{links_str}",
                        title="[bold #8B0000] ВЕСЫ АНУБИСА [/bold #8B0000]", border_style="#8B0000"
                    ))
                else:
                    console.print(f"[bold #8B0000][-] Номер невалиден.[/bold #8B0000]")
            input("\nНажмите Enter, чтобы вернуться в меню...")

        # 3. ПОИСК ПО ГОСНОМЕРУ АВТО
        elif choice == "3":
            target = input("Введите госномер РФ (английскими буквами, например, A777AA77): ").strip()
            if target:
                from modules.car_search import CarScanner
                with console.status("[bold #8B0000][*] Анубис пробивает госномер автомобиля...", spinner="dots",
                                    spinner_style="bold #8B0000"):
                    scanner = CarScanner(target)
                    data = await scanner.scan()

                if data["valid"]:
                    links_str = "\n".join([f"[bold #8B0000]► {link}[/bold #8B0000]" for link in data["links"]])
                    console.print(Panel(
                        f"[bold #8B0000]Цель (Госномер): {data['formatted']}[/bold #8B0000]\n\n"
                        f"[bold #8B0000]▪ Привязка к региону: {data['region_name']}[/bold #8B0000]\n\n"
                        f"[bold #8B0000]Специализированные OSINT-источники:[/bold #8B0000]\n{links_str}",
                        title="[bold #8B0000] ВЕСЫ АНУБИСА [/bold #8B0000]", border_style="#8B0000"
                    ))
                else:
                    console.print(f"[bold #8B0000][-] Ошибка: Неверный формат госномера РФ.[/bold #8B0000]")
            input("\nНажмите Enter, чтобы вернуться в меню...")

        # 4. ПОИСК ПО EMAIL
        elif choice == "4":
            target = input("Введите Email адрес цели (например, target@mail.ru): ").strip()
            if target:
                from modules.email_search import EmailScanner
                with console.status("[bold #8B0000][*] Анубис извлекает цифровой след Email...", spinner="dots",
                                    spinner_style="bold #8B0000"):
                    scanner = EmailScanner(target)
                    data = await scanner.scan()

                if data["valid"]:
                    links_str = "\n".join([f"[bold #8B0000]► {link}[/bold #8B0000]" for link in data["links"]])
                    console.print(Panel(
                        f"[bold #8B0000]Цель: {scanner.email}[/bold #8B0000]\n\n"
                        f"[bold #8B0000]▪ Статус почтового сервера: {data['mx_status']}[/bold #8B0000]\n\n"
                        f"[bold #8B0000]Специализированные OSINT-источники:[/bold #8B0000]\n{links_str}",
                        title="[bold #8B0000] ВЕСЫ АНУБИСА [/bold #8B0000]", border_style="#8B0000"
                    ))
                else:
                    console.print(f"[bold #8B0000][-] Ошибка: Введен некорректный формат Email.[/bold #8B0000]")
            input("\nНажмите Enter, чтобы вернуться в меню...")

        # 5. ПОИСК ПО TELEGRAM
        elif choice == "5":
            target = input("Введите Username или ID цели (например, durov или 93273412): ").strip()
            if target:
                from modules.tg_search import TelegramScanner
                with console.status("[bold #8B0000][*] Анубис извлекает цифровой след Telegram...", spinner="dots",
                                    spinner_style="bold #8B0000"):
                    scanner = TelegramScanner(target)
                    data = await scanner.scan()

                if data["type"] != "Invalid":
                    links_str = "\n".join([f"[bold #8B0000]► {link}[/bold #8B0000]" for link in data["links"]])
                    console.print(Panel(
                        f"[bold #8B0000]Цель: {data['target']}[/bold #8B0000]\n"
                        f"[bold #8B0000]Тип данных: {data['type']}[/bold #8B0000]\n\n"
                        f"[bold #8B0000]Специализированные OSINT-источники:[/bold #8B0000]\n{links_str}",
                        title="[bold #8B0000] ВЕСЫ АНУБИСА [/bold #8B0000]", border_style="#8B0000"
                    ))
                else:
                    console.print(
                        f"[bold #8B0000][-] Ошибка: Введен некорректный формат Telegram ID или Username.[/bold #8B0000]")
            input("\nНажмите Enter, чтобы вернуться в меню...")

        # 0. ВЫХОД
        elif choice == "0":
            console.print("[bold #8B0000]Анубис закрывает врата. До встречи.[/bold #8B0000]")
            break

        else:
            console.print("[bold #8B0000][-] Неверный пункт меню.[/bold #8B0000]")
            await asyncio.sleep(1.5)


if __name__ == "__main__":
    async def do_main():
        try:
            await main()
        except Exception as e:
            console.print(f"[bold #8B0000]\n[-] Критическая ошибка ядра: {e}[/bold #8B0000]")
            input("\nНажмите Enter для выхода...")


    asyncio.run(do_main())






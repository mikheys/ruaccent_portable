

import questionary
from ruaccent import RUAccent
import os
from prompt_toolkit.styles import Style

# --- Глобальные переменные и настройки ---
accentizer = RUAccent()
CACHE_DIR = os.path.dirname(__file__)

# Настройки по умолчанию
settings = {
    "model": "turbo",
    "use_dictionary": True
}

MODELS = ['turbo', 'big_poetry', 'medium_poetry', 'small_poetry']

# Простой стиль для обхода ошибок рендеринга
custom_style = Style([])

# --- Функции ---

def clear_screen():
    """Очищает консоль."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Печатает заголовок программы."""
    print("╔═════════════════════════════════════════════════════════════════════════════╗")
    print("║         Программа для автоматической расстановки ударений в тексте          ║")
    print("║                      Поддерживает многострочный ввод                        ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")
    print(f"Текущая модель: {settings['model']} | Словарь: {'Вкл' if settings['use_dictionary'] else 'Выкл'}")
    print("─"*77)

def load_model():
    """Загружает или перезагружает модель на основе текущих настроек."""
    clear_screen()
    print_header()
    print(f"\nЗагрузка модели: {settings['model']} (Словарь: {'Вкл' if settings['use_dictionary'] else 'Выкл'})...")
    try:
        accentizer.load(
            omograph_model_size=settings['model'], 
            use_dictionary=settings['use_dictionary'], 
            workdir=CACHE_DIR
        )
        print("Модель успешно загружена!")
    except Exception as e:
        print(f"Ошибка при загрузке модели: {e}")
        print("Пожалуйста, проверьте интернет-соединение и попробуйте снова.")
    questionary.press_any_key_to_continue("Нажмите любую клавишу для продолжения...", style=custom_style).ask()

def show_menu():
    """Показывает меню настроек."""
    clear_screen()
    print_header()
    choice = questionary.select(
        "Меню настроек:",
        choices=[
            "Сменить модель",
            "Настройки словаря",
            "Назад к вводу текста"
        ],
        style=custom_style
    ).ask()

    if choice == "Сменить модель":
        new_model = questionary.select("Выберите новую модель:", choices=MODELS, default=settings['model'], style=custom_style).ask()
        if new_model and new_model != settings['model']:
            settings['model'] = new_model
            load_model()
    elif choice == "Настройки словаря":
        use_dict = questionary.confirm("Использовать словарь?", default=settings['use_dictionary'], style=custom_style).ask()
        if use_dict is not None and use_dict != settings['use_dictionary']:
            settings['use_dictionary'] = use_dict
            load_model()

# --- Основной цикл программы ---

def main_loop():
    """Главное меню и цикл работы программы."""
    load_model() # Первоначальная загрузка

    while True:
        clear_screen()
        print_header()
        
        text_to_process = questionary.text(
            message="Введите текст и нажмите Alt+Enter. (!m - меню, !q - выход):",
            multiline=True,
            style=custom_style
        ).ask()

        if text_to_process is None or text_to_process.strip().lower() == '!q':
            print("\nДо свидания!")
            break

        elif text_to_process.strip().lower() == '!m':
            show_menu()

        else:
            result = accentizer.process_all(text_to_process)
            print("\n--- Результат ---")
            print(result)
            print("-----------------")
            questionary.press_any_key_to_continue("Нажмите любую клавишу, чтобы ввести новый текст...", style=custom_style).ask()

if __name__ == "__main__":
    main_loop()

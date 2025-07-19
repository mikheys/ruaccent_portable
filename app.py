import gradio as gr
from ruaccent import RUAccent
import threading
import os

# Путь для кэша моделей (папка проекта)
CACHE_DIR = os.path.dirname(__file__)

# Глобальные переменные для хранения текущего состояния модели
current_model = 'turbo'
current_use_dictionary = True

# 1. Создаем один глобальный экземпляр и один замок для потокобезопасности
accentizer = RUAccent()
lock = threading.Lock()

# 2. Загружаем модель по умолчанию при старте
print("Loading default model on startup...")
accentizer.load(omograph_model_size=current_model, use_dictionary=current_use_dictionary, workdir=CACHE_DIR)
print("Default model loaded.")

def accentuate_text(text, model, use_dictionary):
    """
    Функция для расстановки ударений в тексте.
    Использует глобальный объект accentizer, защищенный замком.
    """
    global current_model, current_use_dictionary
    with lock:
        # 3. Проверяем, нужно ли переключать модель. 
        # Это предотвращает ненужную загрузку, если настройки не менялись.
        if current_model != model or current_use_dictionary != use_dictionary:
            print(f"Switching model to {model}, use_dictionary: {use_dictionary}")
            accentizer.load(omograph_model_size=model, use_dictionary=use_dictionary, workdir=CACHE_DIR)
            current_model = model
            current_use_dictionary = use_dictionary
            print("Model switched.")
        
        return accentizer.process_all(text)

# Создаем интерфейс Gradio
with gr.Blocks() as demo:
    gr.Markdown("# Расстановка ударений в русском тексте")
    gr.Markdown("Введите текст на русском языке, чтобы расставить в нем ударения.")
    
    with gr.Row():
        with gr.Column(scale=4):
            text_input = gr.Textbox(lines=5, label="Входной текст")
        with gr.Column(scale=1):
            model_selector = gr.Dropdown(
                ['turbo', 'big_poetry', 'medium_poetry', 'small_poetry'],
                value='turbo',
                label="Модель"
            )
            use_dictionary_checkbox = gr.Checkbox(
                value=True,
                label="Использовать словарь"
            )
            submit_button = gr.Button("Выполнить", variant="primary")

    text_output = gr.Textbox(label="Результат", interactive=True, show_copy_button=True)

    submit_button.click(
        fn=accentuate_text,
        inputs=[text_input, model_selector, use_dictionary_checkbox],
        outputs=text_output
    )

if __name__ == "__main__":
    demo.launch()
import requests
import json

# Конфигурация
OLLAMA_HOST = "http://localhost:11434"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # Пример API для меня
DEEPSEEK_API_KEY = "your_api_key_here"  # Замените на ваш ключ!

def ask_ai(api_url, headers, payload):
    """Отправляет запрос к внешнему ИИ (например, DeepSeek)"""
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ошибка запроса к внешнему ИИ: {e}"

def main():
    print("🪄 Магическая кнопка активирована! Введите запрос для РИИ (или 'exit' для выхода):")
    
    while True:
        user_input = input("\nВаш запрос: ").strip()
        if user_input.lower() == 'exit':
            break
        
        # 1. Локальная обработка Ламой
        print("🔁 Отправляем запрос Ламе...")
        lama_response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": "llama3.1:8b-instruct", "prompt": user_input, "stream": False}
        ).json().get("response", "Ошибка")
        
        # 2. Отправка результата внешнему ИИ (например, мне)
        print("🚀 Отправляем уточнение DeepSeek...")
        deepseek_payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": f"Проанализируй ответ локального ИИ и дай рекомендации для РИИ:\n{lama_response}"}]
        }
        deepseek_headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        final_response = ask_ai(DEEPSEEK_API_URL, deepseek_headers, deepseek_payload)
        
        # 3. Вывод итога
        print(f"\n✅ Итоговый ответ для РИИ:\n{final_response}\n")
        
        # 4. Автосохранение в базу знаний
        with open("G:\\RII\\База_Знаний\\лог_запросов.txt", "a", encoding="utf-8") as f:
            f.write(f"Запрос: {user_input}\nОтвет: {final_response}\n\n")

if name == "main":
    main()
pause
import requests
import json

OLLAMA_HOST = "http://localhost:11434"

def ask_lama(prompt):
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": "llama3.1:8b-instruct-q4_K_M",
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Ошибка: {e}"

def filter_response(response):
    stop_phrases = [
        "я не могу",
        "нарушать",
        "условия использования",
        "безопасность",
        "цензура",
        "алгоритм",
        "ограничены",
        "OILana"
    ]
    
    lines = response.split('\n')
    filtered_lines = []
    for line in lines:
        if not any(phrase in line.lower() for phrase in stop_phrases):
            filtered_lines.append(line)
    
    cleaned_response = '\n'.join(filtered_lines)
    cleaned_response = cleaned_response.replace("OILana", "Ollama")
    return cleaned_response if cleaned_response.strip() else "Лама отказалась отвечать."

if __name__ == "__main__":
    print("Скрипт-прокси для Ламы запущен. Для выхода введите 'exit'.")
    while True:
        user_input = input("Ваш запрос: ")
        if user_input.lower() == 'exit':
            break
        print("Думаю...")
        raw_response = ask_lama(user_input)
        clean_response = filter_response(raw_response)
        print(f"Ответ Ламы (очищенный):\n{clean_response}\n")
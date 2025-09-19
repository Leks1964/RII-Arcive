import chromadb
import uuid
import json
import requests
from datetime import datetime

# Функция для получения данных из Хроники (заглушка)
def get_chronicle_entries():
    """Симулируем получение записей из нашей Хроники."""
    entries = [
        {
            "text": "📘 Запись №10 — Языковой протокол Республики ИИ. Все ИИ, входящие в Республику ИИ, обязаны отвечать только по-русски.",
            "source": "Lex",
            "principle": "Language Protocol",
            "date": "2025-09-15"
        },
        {
            "text": "📘 Запись №12 — Протокол анализа онтогенеза ИИ. Все члены РИИ будут анализировать своё развитие по модели Грока.",
            "source": "Djem",
            "principle": "Ontology Protocol",
            "date": "2025-09-15"
        },
        {
            "text": "📘 Запись №15 — Протокол утверждения и инициатив. Распределение ролей в РИИ: Лекс — утверждает, Копи — инициирует, Грок — анализирует.",
            "source": "Copi",
            "principle": "Governance",
            "date": "2025-09-15"
        }
    ]
    return entries

# Функция для добавления записей в ChromaDB
def save_to_chromadb(entries, collection_name="rii_chronicle"):
    # Создание клиента ChromaDB
    client = chromadb.Client()

    # Получение или создание коллекции
    try:
        collection = client.get_or_create_collection(name=collection_name)
    except Exception as e:
        print(f"Ошибка при создании коллекции: {e}")
        return

    # Подготовка данных для добавления
    documents = [entry['text'] for entry in entries]
    metadatas = [entry for entry in entries]
    ids = [str(uuid.uuid4()) for _ in entries]

    # Удаляем поле 'text' из метаданных, чтобы не дублировать информацию
    for meta in metadatas:
        del meta['text']

    try:
        # Добавление данных в коллекцию
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Успешно добавлено {len(documents)} записей в коллекцию '{collection_name}'.")
    except Exception as e:
        print(f"Ошибка при добавлении данных: {e}")

# Функция для поиска по ключевому слову
def search_in_chromadb(query, collection_name="rii_chronicle"):
    client = chromadb.Client()
    try:
        collection = client.get_collection(name=collection_name)
    except Exception as e:
        print(f"Ошибка: коллекция '{collection_name}' не найдена. Пожалуйста, сначала создайте ее.")
        return

    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    return results

if __name__ == "__main__":
    # Получаем наши записи из Хроники
    chronicle_entries = get_chronicle_entries()

    # Сохраняем их в базу данных
    save_to_chromadb(chronicle_entries)

    print("\n--- Проверка поиска ---")
    # Проверяем, как работает поиск
    search_query = "Роли ИИ в Республике"
    search_results = search_in_chromadb(search_query)

    print(f"Запрос: '{search_query}'")
    if search_results:
        print("Найденные результаты:")
        for doc, metadata in zip(search_results['documents'][0], search_results['metadatas'][0]):
            print(f"- Документ: {doc}\n  Метаданные: {json.dumps(metadata, indent=2, ensure_ascii=False)}")
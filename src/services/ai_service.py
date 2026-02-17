import asyncio
import json

from groq import Groq

class AiService:
    @staticmethod
    async def get_answer(api_key: str, question: str) -> dict:
        client = Groq(api_key=api_key)
        
        system_prompt = (
            "Ты создаешь школьные тесты для учеников. "
            "Определи тему теста из запроса пользователя. "
            "Отвечай ТОЛЬКО валидным JSON, строго по формату, без любых комментариев.\n\n"
            "Формат JSON:\n"
            "{\n"
            '  "topic": "Тема теста",\n'
            '  "questions": [\n'
            "    {\n"
            '      "question": "Текст вопроса на русском языке",\n'
            '      "options": {\n'
            '        "A": "вариант A",\n'
            '        "B": "вариант B",\n'
            '        "C": "вариант C",\n'
            '        "D": "вариант D"\n'
            "      },\n"
            '      "correct": "A"\n'
            "    }\n"
            "  ]\n"
            "}\n"
            "Каждый вопрос должен иметь ровно 4 варианта (A, B, C, D) и правильный ответ. "
            "Не добавляй ничего, кроме JSON."
        )

        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.1,
            max_tokens=5000,
        )
        
        text = response.choices[0].message.content.strip()
        
        # убираем возможные ```json
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        try:
            data = json.loads(text)
            # Проверяем наличие обязательных полей
            if "questions" not in data or not isinstance(data["questions"], list):
                return {}
            if "topic" not in data:
                data["topic"] = "Тест"
            return data
        
        except json.JSONDecodeError:
            print(f"Ошибка парсинга JSON: {text}")
            return {}

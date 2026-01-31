import asyncio
import json

from groq import Groq

class AiService:
    @staticmethod
    async def get_answer(api_key: str, question: str) -> dict:
        """Функция для создания теста, возвращает строгий JSON"""

        client = Groq(api_key=api_key)
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты создаешь школьные тесты. "
                        "Отвечай ТОЛЬКО валидным JSON без пояснений. "
                        "Формат:\n"
                        "{\n"
                        '  "questions": [\n'
                        "    {\n"
                        '      "question": "Текст вопроса",\n'
                        '      "options": {\n'
                        '        "A": "вариант A",\n'
                        '        "B": "вариант B",\n'
                        '        "C": "вариант C",\n'
                        '        "D": "вариант D"\n'
                        "      },\n"
                        '      "correct": "A"\n'
                        "    }\n"
                        "  ]\n"
                        "}"
                    ),
                },
                {"role": "user", "content": question},
            ],
            temperature=0.7,
            max_tokens=5000,
        )
        
        text = response.choices[0].message.content.strip()
        
        if text.startswith("```json"):
            text = text[7:]

        if text.startswith("```"):
            text = text[3:]
            
        if text.endswith("```"):
            text = text[:-3]
        
        try:
            data = json.loads(text)
            return data["questions"]
        
        except json.JSONDecodeError:
            print(f"Ошибка парсинга JSON: {text}")
            return []
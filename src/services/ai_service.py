class AiService:
    @staticmethod
    async def get_answer(api_key: str, prompt: str) -> dict:
        client = Groq(api_key=api_key)
        
        system_prompt = (
            "Ты создаешь школьные тесты для учеников. "
            "Ты можешь генерировать новые тесты или вносить правки в существующие. "
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
            "Важные правила:\n"
            "1. Каждый вопрос должен иметь ровно 4 варианта (A, B, C, D)\n"
            "2. Правильный ответ указывается буквой (A, B, C или D)\n"
            "3. Если вносятся правки, сохрани структуру, но измени содержание согласно запросу\n"
            "4. Не добавляй ничего, кроме JSON"
        )

        try:
            response = await asyncio.to_thread(
                client.chat.completions.create,
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=10000,
            )
            
            text = response.choices[0].message.content.strip()
            
            if text.startswith("```json"):
                text = text[7:]
            elif text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            
            text = text.strip()
            
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                text = text[start_idx:end_idx]
            
            data = json.loads(text)
            
            if "questions" not in data or not isinstance(data["questions"], list):
                return {}
            if "topic" not in data:
                data["topic"] = "Тест"
                
            for q in data["questions"]:
                if not all(k in q for k in ["question", "options", "correct"]):
                    return {}
                if len(q["options"]) != 4:
                    return {}
                    
            return data
            
        except Exception as e:
            print(f"Ошибка в AiService: {e}")
            print(f"Текст ответа: {text if 'text' in locals() else 'N/A'}")
            return {}
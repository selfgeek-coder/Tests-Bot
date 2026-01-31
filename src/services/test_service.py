from sqlalchemy.orm import Session
from typing import List, Dict, Optional
import json

from src.repositories.test_repository import TestRepository


class TestService:
    @staticmethod
    def get_test(db: Session, slug: str) -> Optional[Dict]:
        """
        Получить тест по его slug

        :param slug: ID Теста
        """

        test = TestRepository.get_test_by_slug(db, slug)
        if not test:
            return None

        return {
            "slug": test.slug,
            "owner_id": test.owner_id,
            "topic": test.topic,
            "questions": json.loads(test.questions),
        }

    @staticmethod
    def get_my_tests(db: Session, owner_id: int) -> List[Dict]:
        """
        Получить свои тесты

        :param db: Сессия в базе данных
        :param owner_id: ID создателя тестов
        """

        tests = TestRepository.get_tests_by_owner(db, owner_id)
        return [
            {
                "slug": t.slug,
                "topic": t.topic,
                "questions_count": len(json.loads(t.questions)),
            }
            for t in tests
        ]

    @staticmethod
    def create_test(
        db: Session,
        slug: str,
        owner_id: int,
        topic: str,
        questions: List[Dict],
    ) -> Dict:
        """
        Создать тест

        :param db: Сессия в базе данных
        :param slug: Уникальный ID теста (SLUG)
        :param owner_id: ID Создателя теста
        :param topic: Тема теста
        :param questions: Массив вопросов теста

        :return: {
            "slug": "123qwe",
            "owner_id": 123,
            "topic": "алгебра 8 класс квадратные корни",
            "questions": "вопросы",
        }
        """

        test = TestRepository.create_test(
            db=db,
            slug=slug,
            owner_id=owner_id,
            topic=topic,
            questions=questions,
        )

        return {
            "slug": test.slug,
            "owner_id": test.owner_id,
            "topic": test.topic,
            "questions": questions,
        }

    @staticmethod
    def delete_test(db: Session, slug: str, owner_id: int) -> bool:
        """
        Удалить тест по его ID
        
        :param db: Сессия в базе данных
        :param slug: Уникальный ID теста
        :param owner_id: ID Создателя теста
        """

        test = TestRepository.get_test_by_slug(db, slug)

        # является ли создателем теста
        if not test or test.owner_id != owner_id:
            return False

        TestRepository.delete_test(db, test)
        return True
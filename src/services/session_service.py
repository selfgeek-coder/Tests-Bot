from typing import Optional, Dict
import json

from sqlalchemy.orm import Session

from src.repositories.session_repository import SessionRepository
from src.repositories.result_repository import ResultRepository
from src.repositories.test_repository import TestRepository


class SessionService:
    @staticmethod
    def start_session(db: Session, user_id: int, slug: str, fullname: str):
        """
        Создать новую сессию для прохождения теста

        :param db: Сессия в базе данных
        :param user_id: ID пользователя
        :param slug: Уникальный ID теста
        :param fullname: ФИО пользователя
        """
        
        return SessionRepository.create_session(db, user_id, slug, fullname)

    @staticmethod
    def can_start_test(db, user_id: int, slug: str) -> bool:
        """
        Проверка: можно ли начать тест
        
        :param user_id: ID пользователя
        :param slug: ID теста
        """
        
        exist = ResultRepository.get_result(db, user_id, slug)
        return exist is None

    @staticmethod
    def get_session(db: Session, user_id: int) -> Optional[Dict]:
        """
        Получить сессию прохождения

        :param db: Сессия в базе данных
        :param user_id: ID пользователя

        :return: {
            "user_id": 123,
            "slug": "123qwe",
            "fullname": "Иван Иванович Иван",
            "question_index": 1,
            "score": 0,
        }
        """

        session = SessionRepository.get_session(db, user_id)
        if not session:
            return None

        return {
            "user_id": session.user_id,
            "slug": session.slug,
            "fullname": session.fullname,
            "question_index": session.question_index,
            "score": session.score,
        }

    @staticmethod
    def update_session(db: Session, user_id: int, question_index: int, score: int):
        """
        Обновить сессию

        :param db: Сессия в базе данных
        :param user_id: ID пользователя
        :param question_index: Index вопроса
        :param score: Набранные очки (баллы)
        """

        SessionRepository.update_session(db, user_id, question_index, score)

    @staticmethod
    def finish_test(db: Session, user_id: int):
        """
        Завершить тест

        :param db: Сессия в базе данных
        :param user_id: ID пользователя
        """
        session = SessionRepository.get_session(db, user_id)
        if not session:
            return

        test = TestRepository.get_test_by_slug(db, session.slug)
        questions = json.loads(test.questions)

        ResultRepository.save_result(
            db=db,
            slug=session.slug,
            user_id=session.user_id,
            fullname=session.fullname,
            score=session.score,
            max_score=len(questions),
        )

        SessionRepository.delete_session(db, user_id)
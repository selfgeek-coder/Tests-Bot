from typing import Optional
from sqlalchemy.orm import Session
from src.db.models import ActiveSession


class SessionRepository:

    @staticmethod
    def get_session(db: Session, user_id: int) -> Optional[ActiveSession]:
        return (
            db.query(ActiveSession)
            .filter(ActiveSession.user_id == user_id)
            .first()
        )

    @staticmethod
    def create_session(
        db: Session,
        user_id: int,
        slug: str,
        fullname: str
    ) -> ActiveSession:
        session = ActiveSession(
            user_id=user_id,
            slug=slug,
            fullname=fullname,
            question_index=0,
            score=0
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def get_or_create_session(
        db: Session,
        user_id: int,
        slug: str,
        fullname: str
    ) -> ActiveSession:
        existing = SessionRepository.get_session(db, user_id)

        if existing:
            return existing  # уже есть активная сессия

        return SessionRepository.create_session(db, user_id, slug, fullname)

    @staticmethod
    def update_session(
        db: Session,
        user_id: int,
        question_index: int,
        score: int
    ):
        session = SessionRepository.get_session(db, user_id)

        if session:
            session.question_index = question_index
            session.score = score
            db.commit()

    @staticmethod
    def delete_session(db: Session, user_id: int):
        session = SessionRepository.get_session(db, user_id)

        if session:
            db.delete(session)
            db.commit()

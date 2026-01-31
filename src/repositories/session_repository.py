from sqlalchemy.orm import Session
from typing import Optional
from src.db.models import ActiveSession


class SessionRepository:
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
            fullname=fullname
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return session

    @staticmethod
    def get_session(db: Session, user_id: int) -> Optional[ActiveSession]:
        return (
            db.query(ActiveSession)
            .filter(ActiveSession.user_id == user_id)
            .first()
        )

    @staticmethod
    def update_session(
        db: Session,
        user_id: int,
        question_index: int,
        score: int
    ):
        session = db.query(ActiveSession).filter(
            ActiveSession.user_id == user_id
        ).first()

        if session:
            session.question_index = question_index
            session.score = score
            db.commit()

    @staticmethod
    def delete_session(db: Session, user_id: int):
        session = db.query(ActiveSession).filter(
            ActiveSession.user_id == user_id
        ).first()

        if session:
            db.delete(session)
            db.commit()

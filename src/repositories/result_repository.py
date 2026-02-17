from sqlalchemy.orm import Session

from src.db.models import TestResult, Test


class ResultRepository:
    @staticmethod
    def save_result(
        db: Session,
        slug: str,
        user_id: int,
        fullname: str,
        score: int,
        max_score: int,
    ):
        result = TestResult(
            slug=slug,
            user_id=user_id,
            fullname=fullname,
            score=score,
            max_score=max_score,
        )
        db.add(result)
        db.commit()

    @staticmethod
    def get_results_by_test(db: Session, slug: str):
        return (
            db.query(TestResult)
            .filter(TestResult.slug == slug)
            .order_by(TestResult.finished_at.desc())
            .all()
        )
        
    @staticmethod
    def get_result(db: Session, user_id: int, slug: str):
        return db.query(TestResult).filter(
            TestResult.user_id == user_id,
            TestResult.slug == slug
        ).first()
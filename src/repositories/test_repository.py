from typing import Optional, List
import json

from sqlalchemy.orm import Session

from src.db.models import Test


class TestRepository:
    @staticmethod
    def get_test_by_slug(db: Session, slug: str) -> Optional[Test]:
        return db.query(Test).filter(Test.slug == slug).first()

    @staticmethod
    def get_tests_by_owner(db: Session, owner_id: int) -> List[Test]:
        return db.query(Test)\
                .filter(Test.owner_id == owner_id)\
                .order_by(Test.created_at.desc())\
                .all()


    @staticmethod
    def delete_test(db: Session, test: Test) -> None:
        db.delete(test)
        db.commit()

    @staticmethod
    def create_test(db: Session, slug: str, owner_id: int, topic: str, questions: list) -> Test:
        test = Test(
            slug=slug,
            owner_id=owner_id,
            topic=topic,
            questions=json.dumps(questions)
        )
        db.add(test)
        db.commit()
        db.refresh(test)
        
        return test

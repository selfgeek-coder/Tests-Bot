from sqlalchemy.orm import Session
from typing import Optional, List
from src.db.models import Test
import json


class TestRepository:
    @staticmethod
    def get_test_by_slug(db: Session, slug: str) -> Optional[Test]:
        return db.query(Test).filter(Test.slug == slug).first()

    @staticmethod
    def get_tests_by_owner(db: Session, owner_id: int) -> List[Test]:
        return db.query(Test).filter(Test.owner_id == owner_id).all()

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

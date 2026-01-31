from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# таблица для хранений тестов
class Test(Base):
    __tablename__ = "tests"

    slug = Column(String, primary_key=True)
    owner_id = Column(Integer, nullable=False)
    topic = Column(String, nullable=False)
    questions = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    sessions = relationship(
        "ActiveSession",
        back_populates="test",
        cascade="all, delete-orphan"
    )
    results = relationship(
        "TestResult",
        back_populates="test",
        cascade="all, delete-orphan"
    )


# таблица активных прохождений тестов
class ActiveSession(Base):
    __tablename__ = "active_sessions"

    user_id = Column(Integer, primary_key=True)
    slug = Column(String, ForeignKey("tests.slug"), nullable=False)
    fullname = Column(String, nullable=False)

    question_index = Column(Integer, default=0)
    score = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    test = relationship("Test", back_populates="sessions")


# таблица результатов тестирований
class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String, ForeignKey("tests.slug"), nullable=False)
    user_id = Column(Integer, nullable=False)
    fullname = Column(String, nullable=False)

    score = Column(Integer, nullable=False)
    max_score = Column(Integer, nullable=False)

    finished_at = Column(TIMESTAMP, default=datetime.utcnow)

    test = relationship("Test", back_populates="results")

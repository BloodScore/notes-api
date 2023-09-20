from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import settings


DATABASE_URL = settings.DATABASE_URL


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

Base = declarative_base()


def get_db_session():
    db_session = Session()

    try:
        yield db_session
    finally:
        db_session.close()


class CRUDMixin:
    @classmethod
    def set_db_session(cls, db_session):
        cls.db_session = db_session

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def get(cls, **kwargs):
        result = cls.db_session.query(cls)

        for attr, value in kwargs.items():
            result = result.filter(getattr(cls, attr) == value)

        return result.first()

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save()

    def save(self):
        self.db_session.add(self)
        self.db_session.commit()
        return self

    def delete(self):
        self.db_session.delete(self)
        self.db_session.commit()


class BaseModel(CRUDMixin, Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

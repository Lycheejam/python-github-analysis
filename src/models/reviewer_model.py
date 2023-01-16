from datetime import datetime
from sqlalchemy import DATETIME, Column, Integer, String

from models.setting import Base, engine


class Reviewer(Base):

    __tablename__ = "reviewers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reviewer_id = Column(Integer)
    pullrequest_id = Column(Integer)
    submitted_at = Column(DATETIME)
    submitted_by = Column(String(255))
    state = Column(String(255))
    created_at = Column(DATETIME, default=datetime.now, nullable=False)
    updated_at = Column(DATETIME, default=datetime.now, nullable=False)


Base.metadata.create_all(bind=engine)

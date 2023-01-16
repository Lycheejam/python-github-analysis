from datetime import datetime
from sqlalchemy import DATETIME, Column, Integer, String

from models.setting import Base, engine


class PullRequest(Base):

    __tablename__ = "pullrequests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    repo = Column(String(255))
    p_id = Column(Integer)
    p_number = Column(Integer)
    base_ref = Column(String(255))
    head_ref = Column(String(255))
    p_created_at = Column(DATETIME)
    p_create_by = Column(String(255))
    merged_at = Column(DATETIME)
    merged_by = Column(String(255))
    closed_at = Column(DATETIME)
    created_at = Column(DATETIME, default=datetime.now, nullable=False)
    updated_at = Column(DATETIME, default=datetime.now, nullable=False)


Base.metadata.create_all(bind=engine)

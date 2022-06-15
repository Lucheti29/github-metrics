from sqlalchemy import Column, Integer, String, Date, DateTime, Float

from utils.sql import Base

class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True, index=True)
    repository_name = Column(String, nullable=False)
    pull_request_id = Column(Integer, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    github_user = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
    closed_at = Column(DateTime)
    reviews_count = Column(Integer, nullable=False)
    time_to_close = Column(Integer, default=0)
    status = Column(String, nullable=False)
    additions = Column(Integer, default=0)
    deletions = Column(Integer, default=0)
    commits = Column(Integer, default=0)
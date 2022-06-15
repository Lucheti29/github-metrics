from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date

class PullRequestBase(BaseModel):
    id: int
    repository_name: str
    pull_request_id: int
    title: str
    url: str
    github_user: str
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime]
    reviews_count: int
    status: str
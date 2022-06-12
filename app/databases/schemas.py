from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date

## -------- Contributors --------

class ContributorBase(BaseModel):
    email: str
    name: str
    lastname: str
    startdate: date
    enddate: Optional[date] = None

class ContributorCreate(ContributorBase):
    pass

class ContributorUpdate(ContributorBase):
    pass

## -------- Pull request --------

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
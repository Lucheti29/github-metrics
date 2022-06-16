from databases import models
from sqlalchemy.orm import Session
from utils import date_utils

## TODO: Create bulk class

def get_all_pull_requests(db: Session):
    return db.query(models.PullRequest).all()

def map_pull_request(pull, repository_name: str):
    return {
        "repository_name": repository_name,
        "pull_request_id": pull.id,
        "title": pull.title,
        "url": pull.url,
        "github_user": pull.user.login,
        "created_at": pull.created_at,
        "updated_at": pull.updated_at,
        "closed_at": pull.closed_at, 
        "reviews_count": pull.get_reviews().totalCount,
        "status": "closed",
        "time_to_close": date_utils.time_between_dates_in_seconds(pull.closed_at, pull.created_at),
        "additions": pull.additions,
        "deletions": pull.deletions,
        "commits": pull.commits
    }

def bulk_new_pull_request(db: Session, prs):
    db.bulk_insert_mappings(models.PullRequest, prs)
    db.commit()

def update_pull_request(model: models.PullRequest, pull, db: Session):
    model.title = pull.title
    model.url = pull.url
    model.updated_at = pull.updated_at
    model.closed_at = pull.closed_at
    model.reviews_count = pull.get_reviews().totalCount
    model.status = pull.status
    model.time_to_close = date_utils.time_between_dates_in_seconds(pull.closed_at, pull.created_at)
    model.github_user = pull.user.login
    model.additions = pull.additions
    model.deletions = pull.deletions
    model.commits = pull.commits

    db.commit()
    db.refresh(model)
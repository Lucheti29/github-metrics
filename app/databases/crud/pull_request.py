from databases import models
from sqlalchemy.orm import Session

def get_all_pull_requests(db: Session):
    return db.query(models.PullRequest).all()

def create_pull_request(db: Session, **kwargs):
    model = models.PullRequest(
        repository_name = kwargs['repository_name'],
        pull_request_id = kwargs['pull_request_id'],
        title = kwargs['title'],
        url = kwargs['url'],
        github_user = kwargs['github_user'],
        created_at = kwargs['created_at'],
        updated_at = kwargs['updated_at'],
        closed_at = kwargs['closed_at'], 
        reviews_count = kwargs['reviews_count'],
        status = kwargs['status'])

    db.add(model)
    db.commit()

def update_pull_request(model: models.PullRequest, db: Session, **kwargs):
    model.title = kwargs['title']
    model.url = kwargs['url']
    model.updated_at = kwargs['updated_at']
    model.closed_at = kwargs['closed_at']
    model.reviews_count = kwargs['reviews_count']
    model.status = kwargs['status']

    db.commit()
    db.refresh(model)
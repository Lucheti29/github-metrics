from databases import models
from sqlalchemy.orm import Session

## TODO: Create bulk class

def get_all_pull_requests(db: Session):
    return db.query(models.PullRequest).all()

def bulk_new_pull_request(db: Session, prs):
    db.bulk_insert_mappings(models.PullRequest, prs)
    db.commit()

def update_pull_request(model: models.PullRequest, db: Session):
    db.commit()
    db.refresh(model)
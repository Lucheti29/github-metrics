from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from databases.models import PullRequest
from databases import models
from databases.crud import pull_request as pr_crud
from utils import sql
from datetime import datetime
import pandas as pd
from utils.config import get_settings

from github import Github

## Router config
router = APIRouter(
    prefix="/metrics",
    tags=["metrics"],
    responses={404: {"description": "Not found"}},
)

TOKEN = get_settings().GITHUB_TOKEN
ORGANIZATION_NAME = get_settings().GITHUB_ORGANIZATION
LIMIT_REPOS = 2
LIMIT_PULLS_PER_REPO = 5
THRESHOLD_CR_HOURS = 8

            #diff = datetime.now() - pull.created_at
            #diff_in_hours = diff.total_seconds() / 3600

            #row['pull_time_open'] = diff_in_hours

            #data.append(row)

    #df = pd.DataFrame(data)
    #df.to_csv('pr_open_metrics.csv')

@router.get("/open_pulls", status_code=200)
async def get_open_pulls(db: Session = Depends(sql.get_db)):
    g = Github(TOKEN)
    
    prs_dict = _get_all_prs(db)

    for repo in g.get_organization(ORGANIZATION_NAME).get_repos():
        print(f"------- Repo name -> {repo.name} -------")

        for pull in repo.get_pulls(state="open", sort="created"):
            # Check the new pull requests created
            if pull.id not in prs_dict:
                _create_pull_request(repo.name, pull, "open", db)

            # Update the pull requests already created in status open
            elif pull.updated_at > prs_dict[pull.id].updated_at:
                _update_pull_request(prs_dict[pull.id], pull, "open", db)

@router.get("/closed_pulls", status_code=200)
async def get_closed_pulls(db: Session = Depends(sql.get_db)):
    g = Github(TOKEN)

    prs_dict = _get_all_prs(db)

    for repo in g.get_organization(ORGANIZATION_NAME).get_repos():
        print(f"------- Repo name -> {repo.name} -------")

        for pull in repo.get_pulls(state="closed", sort="updated", direction="desc"):
            if pull.is_merged:
                if pull.id not in prs_dict:
                    _create_pull_request(repo.name, pull, "closed", db)

                elif pull.updated_at > prs_dict[pull.id].updated_at:
                    _update_pull_request(prs_dict[pull.id], pull, "closed", db)

                else:
                    break

@router.get("/generate_csv", status_code=200)
async def generate_csv(db: Session = Depends(sql.get_db)):
    data = []

    for row in pr_crud.get_all_pull_requests(db):
        data.append(row.__dict__)

    df = pd.DataFrame(data)
    df = df.drop(['_sa_instance_state'], axis=1)
    df.to_csv('prs.csv')


## Convert the rows into a dict with pull request id as key and the object as value
def _get_all_prs(db: Session):
    return { row.pull_request_id: row for row in pr_crud.get_all_pull_requests(db) }

def _create_pull_request(repo_name: str, pull: PullRequest, status: str, db: Session):
    pr_crud.create_pull_request(db, 
        repository_name = repo_name,
        pull_request_id = pull.id,
        title = pull.title,
        url = pull.url,
        github_user = pull.user.login,
        created_at = pull.created_at,
        updated_at = pull.updated_at,
        closed_at = pull.closed_at, 
        reviews_count = pull.get_reviews().totalCount,
        status = status
    )

def _update_pull_request(model: models.PullRequest, pull: PullRequest, status: str, db: Session):
    pr_crud.update_pull_request(model, db,
        title = pull.title,
        url = pull.url,
        updated_at = pull.updated_at,
        closed_at = pull.closed_at, 
        reviews_count = pull.get_reviews().totalCount,
        status = status
    )
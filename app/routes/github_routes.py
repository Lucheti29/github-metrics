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
REPOS = [""]


@router.get("/open_pulls", status_code=200)
async def get_open_pulls(db: Session = Depends(sql.get_db)):
    open_pulls = []
    old_pulls = _get_all_prs(db) ## It's a dict

    for repo in _get_repos(Github(TOKEN)):
        for pr in repo.get_pulls(state="open", sort="created"):
            if pr.id not in old_pulls:
                open_pulls.append(_map_pull_request(pr, repo.name))

    pr_crud.bulk_new_pull_request(db, open_pulls)


@router.get("/closed_pulls", status_code=200)
async def get_closed_pulls(db: Session = Depends(sql.get_db)):
    open_pulls = []
    closed_pulls = []
    old_pulls = _get_all_prs(db) ## It's a dict

    for repo in _get_repos(Github(TOKEN)):
        print(f"------ Repo name {repo.name} ------")
        pulls = repo.get_pulls(state="closed", sort="updated", direction="desc")
        total = pulls.totalCount
        index = 1

        for pr in pulls:
            print(f"Pull requests: {index}/{total}")

            if pr.is_merged:
                if pr.id not in old_pulls:
                    open_pulls.append(_map_pull_request(pr, repo.name))

                elif pr.updated_at > old_pulls[pr.id].updated_at:
                    _update_pull_request(old_pulls[pull.id], pr, "closed", db)

                else:
                    ## Break the cycle because the next ones are updated
                    print("Old data reached. Next...")
                    break

            index += 1

    pr_crud.bulk_new_pull_request(db, open_pulls)


@router.get("/generate_csv", status_code=200)
async def generate_csv(db: Session = Depends(sql.get_db)):
    _generate_csv(pr_crud.get_all_pull_requests(db), 'prs.csv')


#######################################
########### Private methods ###########
#######################################

## Convert the rows into a dict with pull request id as key and the object as value
def _get_all_prs(db: Session):
    return { row.pull_request_id: row for row in pr_crud.get_all_pull_requests(db) }

def _map_pull_request(pr: PullRequest, repository_name: str):
    return {
        "repository_name": repository_name,
        "pull_request_id": pr.id,
        "title": pr.title,
        "url": pr.url,
        "github_user": pr.user.login,
        "created_at": pr.created_at,
        "updated_at": pr.updated_at,
        "closed_at": pr.closed_at, 
        "reviews_count": pr.get_reviews().totalCount,
        "status": "closed",
        "time_to_close": _time_between_dates_in_seconds(pull.closed_at, pull.created_at),
        "additions": pr.additions,
        "deletions": pr.deletions,
        "commits": pr.commits
    }

def _update_pull_request(model: models.PullRequest, pull: PullRequest, status: str, db: Session):
    model.title = pull.title
    model.url = pull.url
    model.updated_at = pull.updated_at
    model.closed_at = pull.closed_at
    model.reviews_count = pull.get_reviews().totalCount
    model.status = pull.status
    model.time_to_close = _time_between_dates_in_seconds(pull.closed_at, pull.created_at)
    model.github_user = pull.user.login
    model.additions = pull.additions
    model.deletions = pull.deletions
    model.commits = pull.commits

    pr_crud.update_pull_request(model, db)


def _time_between_dates_in_seconds(d1, d2):
    return abs((d1 - d2).seconds)


def _generate_csv(rows, file_name):
    if len(rows) <= 0:
        print("No rows to generate a csv")
        return

    data = []

    for row in rows:
        data.append(row.__dict__)

    df = pd.DataFrame(data)
    df = df.drop(['_sa_instance_state'], axis=1)
    df.to_csv(file_name)

def _get_repos(github):
    repos = []

    for repo in github.get_organization(ORGANIZATION_NAME).get_repos():
        if repo.name in REPOS:
            repos.append(repo)

    return repos
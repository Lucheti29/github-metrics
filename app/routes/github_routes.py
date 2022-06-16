from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from databases.models import PullRequest
from databases import models
from databases.crud import pull_request as pr_crud
from utils import sql, file_utils, date_utils
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
REPOS = []

@router.get("/pull_requests", status_code=200)
async def get_closed_pulls(db: Session = Depends(sql.get_db)):
    for repo in _get_repos(Github(TOKEN)):
        print(f"------ Repo name {repo.name} ------")
        _parse_prs_data(db, repo.name, repo.get_pulls(state="open", sort="created"))
        _parse_prs_data(db, repo.name, repo.get_pulls(state="closed", sort="updated", direction="desc"))


@router.get("/generate_csv", status_code=200)
async def generate_csv(db: Session = Depends(sql.get_db)):
    file_utils.generate_csv(pr_crud.get_all_pull_requests(db), 'prs.csv')


#######################################
########### Private methods ###########
#######################################

def _parse_prs_data(db, repo_name, pulls):
    ## Convert the rows into a dict with pull request id as key and the object as value
    old_pulls = { row.pull_request_id: row for row in pr_crud.get_all_pull_requests(db) }
    new_pulls_to_push = []
    total = pulls.totalCount
    index = 1

    for pr in pulls:
        print(f"Pull requests: {index}/{total}")

        if pr.is_merged:
            if pr.id not in old_pulls:
                new_pulls_to_push.append(pr_crud.map_pull_request(pr, repo_name))

            elif pr.updated_at > old_pulls[pr.id].updated_at:
                pr_crud.update_pull_request(old_pulls[pull.id], pr, db)

            else:
                ## Break the cycle because the next ones are updated
                print("Old data reached. Next...")
                break

        index += 1

    pr_crud.bulk_new_pull_request(db, new_pulls_to_push)

def _get_repos(github):
    repos = []

    for repo in github.get_organization(ORGANIZATION_NAME).get_repos():
        if repo.name in REPOS:
            repos.append(repo)

    return repos
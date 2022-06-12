from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from databases import crud, schemas
from utils import sql

## Router config
router = APIRouter(
    prefix="/contributors",
    tags=["contributors"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=201)
async def create_contributor(body: schemas.ContributorCreate, db: Session = Depends(sql.get_db)):
    return crud.create_contributor(body, db)

@router.get("/{id}", status_code=200)
async def get_contributor(id: int, db: Session = Depends(sql.get_db)):
    model = crud.get_contributor(id, db)

    if model is None:
        raise HTTPException(status_code=404, detail="Contributor not found")

    return model

@router.get("/", status_code=200)
async def get_contributors(db: Session = Depends(sql.get_db)):
    return crud.get_contributors(db)

@router.put("/{id}", status_code=204)
async def update_contributor(id: int, body: schemas.ContributorUpdate, db: Session = Depends(sql.get_db)):
    if crud.update_contributor(id, body, db) is not True:
        raise HTTPException(status_code=404, detail="Contributor not found")

@router.delete("/{id}", status_code=204)
async def delete_contributor(id: int, db: Session = Depends(sql.get_db)):
    if crud.delete_contributor(id, db) is not True:
        raise HTTPException(status_code=404, detail="Contributor not found")
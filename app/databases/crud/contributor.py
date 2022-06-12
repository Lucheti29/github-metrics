from databases import models, schemas
from sqlalchemy.orm import Session
from utils import sql

## -------- Contributors --------

def create_contributor(schema: schemas.ContributorCreate, db: Session):
    model = models.Contributor(
        email = schema.email, 
        name = schema.name, 
        lastname = schema.lastname,
        startdate = schema.startdate,
        enddate = schema.enddate)

    db.add(model)
    db.commit()
    db.refresh(model)

    return model

def get_contributor(id: int, db: Session):
    return db.query(models.Contributor).get(id)

def get_contributors(db: Session):
    return db.query(models.Contributor).all()

def update_contributor(id: int, schema: schemas.ContributorUpdate, db: Session):
    model = db.query(models.Contributor).get(id)

    if model is not None:
        model.email = schema.email
        model.name = schema.name
        model.lastname = schema.lastname
        model.startdate = schema.startdate
        model.enddate = schema.enddate
        db.commit()
        return True
    
    return False

def delete_contributor(id: int, db: Session) -> bool:
    model = db.query(models.Contributor).get(id)

    if model is not None:
        db.delete(model)
        db.commit()
        return True

    return False

## -------- Squad --------
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.core.security import create_access_token, get_current_user, verify_password
from app.db import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=schemas.TokenOut)
def login(body: schemas.LoginIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == body.username).first()
    if not user or not user.is_active or not verify_password(body.password, user.password_hash):
        raise HTTPException(401, "Incorrect username or password")
    return schemas.TokenOut(
        access_token=create_access_token(user.username), username=user.username, role=user.role
    )


@router.get("/me")
def me(user: models.User = Depends(get_current_user)):
    return {"username": user.username, "role": user.role, "group_id": user.group_id}


@router.get("/groups", response_model=list[schemas.GroupOut])
def groups(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    q = db.query(models.Group)
    if user.group_id:
        q = q.filter(models.Group.id == user.group_id)
    return q.order_by(models.Group.name).all()

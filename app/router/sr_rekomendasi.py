from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from itsdangerous import URLSafeSerializer
from app.schemas.user import *
from app.schemas.donasi import *
from app.schemas.response import *
from app.crud.donasi import *
from app.crud.user import *
from app.db.session import get_db
from app.models.user import *
from app.models.donasi import *


sr = APIRouter()



@sr.get("/rekomendasi/getData", tags=["recomendation system"])
def rekomendasi():
    pass
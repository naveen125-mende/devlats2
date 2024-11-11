#app/routes/routes.py
import uvicorn, os
from fastapi import FastAPI, Depends, HTTPException,APIRouter
from models.schemas import UserSchema, UserLoginSchema
from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer
from motor.motor_asyncio import AsyncIOMotorClient
from mongodb import db

router = APIRouter()
@router.get("/", tags=["home"])
def home():
    return {"message": "Welcome to Naveen's application"}

@router.put("/signup/", tags=["user"])
async def create_user(user: UserSchema, db: AsyncIOMotorClient = Depends(lambda: db)):
    cur_user = await db.users.find_one({"email": user.email})
    if cur_user:
        raise HTTPException(status_code=400, detail="Email already registered")     
    user_dict = user.dict(exclude={"confirm_password"})
    
    await db.users.insert_one(user_dict)
    return {"message": "You are successfully signed up, login for JWT token"}

@router.post("/login/", tags=["user"])
async def user_login(user: UserLoginSchema, db: AsyncIOMotorClient = Depends(lambda: db)):
    stored_user = await db.users.find_one({"email": user.email})
    if not stored_user:
        raise HTTPException(status_code=401, detail="Wrong email!")
    if user.password != stored_user["password"]:
        raise HTTPException(status_code=401, detail="Wrong password!")
    return signJWT(user.email)

@router.get("/protected/", dependencies=[Depends(JWTBearer())], tags=["protected"])
async def protected_route():
    return {"message": "You are viewing a protected token"}

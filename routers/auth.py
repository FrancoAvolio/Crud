from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["auth"])
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserInDB(User):
    password: str

users_db = {
    "user1": {
        "username": "JohnD",
        "full_name": "John Doe",
        "email": "john@example.com",
        "disabled": False,
        "password": "XXXXXXXX"
    },
    "user2": {
        "username": "JaneD",
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "disabled": True,
        "password": "123456"
    },
}
def search_user_db(username: str):
    for user in users_db.values():
        if user["username"] == username:
            return UserInDB(**user)
    return None

def search_user(username: str):
    for user in users_db.values():
        if user["username"] == username:
            return User(**user)
    return None

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User disabled")
    return user
    

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user_db(form.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username",
        headers={"WWW-Authenticate": "Bearer"})
    if form.password != user.password:
        raise HTTPException(status_code=400, detail="Incorrect password", headers={"WWW-Authenticate": "Bearer"})
    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
   




   

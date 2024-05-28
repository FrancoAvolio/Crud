from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

router = APIRouter(prefix="/api", tags=["auth"])
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserInDB(User):
    password: str

users_db = {
    "JohnD": {
        "username": "JohnD",
        "full_name": "John Doe",
        "email": "john@example.com",
        "disabled": False,
        "password": "$2a$12$2sN6mAmns2YEy00byZmtX.dCrvCVQ/0Ulo7hMIXYd/SRubcjCMeim"
    },
    "JaneD": {
        "username": "JaneD",
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "disabled": True,
        "password": "$2a$12$ZYCjIomh/iqJpdMNuzKexeR8RFHFJPB6LWak4ZAKtk1O6zz4D.KgC"
    },
}

def search_user_db(username: str):
    user = users_db.get(username)
    if user:
        return UserInDB(**user)
    return None

def search_user(username: str):
    user = users_db.get(username)
    if user:
        return User(**user)
    return None

async def auth_user(token: str = Depends(oauth2)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: no subject", headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: JWT error", headers={"WWW-Authenticate": "Bearer"})

    user = search_user(username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found", headers={"WWW-Authenticate": "Bearer"})
    
    return user

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User disabled")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user_db(form.username)
    if user is None or not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + access_token_expires
    access_token = jwt.encode(
        {"sub": user.username, "exp": expire},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
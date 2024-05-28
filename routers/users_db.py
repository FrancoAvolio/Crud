from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/userdb", tags=["userdb"])

class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int

users_list = [User(id=1234, name="Franco",surname="Avolio", age=22),
            User(id=4568, name="Jose",surname="Avolio", age=22),
            User(id=1111, name="XD",surname="Avolio", age=22)]  

@router.get("/")
async def users():
    return users_list
 

@router.get("/{id}")
async def user_by_id(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        raise HTTPException(status_code=404, detail="Id not found")
    

@router.get("/query/")
async def user_by_query(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try: 
        return list(users)[0]
    except:
        raise HTTPException(status_code=404, detail="Id not found")
    

@router.post("/")
async def create_user(user: User):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    users_list.append(user)
    return user


@router.put("/")
async def update_user(user: User):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            return user
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    

@router.delete("/{id}")
async def delete_user(id: int):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            return "User deleted"
    if not id:
        raise HTTPException(status_code=404, detail="User not found")

    
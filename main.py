from fastapi import FastAPI
from routers import products, users, jwt, auth, users_db

from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt.router)
app.include_router(auth.router)
app.include_router(users_db.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/url")
async def main():
    return {"url": "http://127.0.0.1:8000/docs#/"}
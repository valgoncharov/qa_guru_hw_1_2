import json
from http import HTTPStatus
import uvicorn
from fastapi_pagination import Page, add_pagination, paginate
from fastapi import FastAPI, HTTPException

from models.User import User
from models.AppStatus import AppStatus


app = FastAPI()
add_pagination(app)

# Global variable to store users
users: list[User] = []


def load_users():
    global users
    with open("users.json") as f:
        users_data = json.load(f)
    users = [User.model_validate(user) for user in users_data]


@app.on_event("startup")
async def startup_event():
    load_users()


@app.get("/status",  summary='Статус приложения', tags=['Healthcheck'], status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=len(users) > 0)


@app.get("/users/{user_id}", summary='Просмотр данных пользователя', tags=['Admin'], status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")

    # Find user by ID
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="User not found")
    return user


@app.get("/users", summary='Просмотр данных всех пользователей', tags=['Admin'], status_code=HTTPStatus.OK)
def get_users() -> Page[User]:
    return paginate(users)


@app.get("/users_all", summary='Просмотр данных всех пользователей', tags=['Admin'], status_code=HTTPStatus.OK)
def get_all_users() -> list[User]:
    return users


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

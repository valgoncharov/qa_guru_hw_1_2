import json
from http import HTTPStatus
from fastapi_pagination import Page, add_pagination, paginate
from fastapi import FastAPI, HTTPException
from models.users_model import UserData
from models.AppStatus import AppStatus
import uvicorn

app = FastAPI()
add_pagination(app)

users: list[UserData] = []


@app.get("/status",  summary='Статус приложения', tags=['Healthcheck'], status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=bool(users))


@app.get("/api/users/{user_id}", summary='Просмотр данных пользователя', tags=['Admin'], status_code=HTTPStatus.OK)
async def get_user(user_id: int) -> UserData:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    if user_id > len(users):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return users[user_id - 1]


@app.get("/api/users/", summary='Просмотр данных пользователей', tags=['Admin'], status_code=HTTPStatus.OK)
def get_users() -> Page[UserData]:
    return paginate(users)


if __name__ == "__main__":

    with open("users.json") as f:
        users = json.load(f)

    for user in users:
        UserData.model_validate(user)

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)


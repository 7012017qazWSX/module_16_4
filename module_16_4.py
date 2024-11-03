from fastapi import FastAPI, Path, HTTPException
from typing import Annotated, List, Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    id: Optional[int] = None
    username: str = Field(..., min_length=3, max_length=15, description='Введите имя пользователя', example='User')
    age: int = Field(..., ge=18, le=120, description='Введите возраст', example=22)


app = FastAPI()
users: List[User] = []


def get_user_index(user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            return i
    raise HTTPException(status_code=404, detail=f'User {user_id} was not found')


@app.get('/users')
async def get_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def add_user(
    username: Annotated[str, Path(min_length=3, max_length=15, description='Введите имя пользователя', example='User')],
    age: Annotated[int, Path(ge=18, le=120, description='Введите возраст', example=22)]
) -> User:
    user_id = users[-1].id + 1 if users else 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
    user_id: Annotated[int, Path(ge=1, le=100, description='Введите id пользователя', example=1)],
    username: Annotated[str, Path(min_length=3, max_length=15, description='Введите имя пользователя', example='UrbanUser')],
    age: Annotated[int, Path(ge=18, le=120, description='Введите возраст', example=25)]
) -> User:
    user_ind = get_user_index(user_id)
    users[user_ind].username = username
    users[user_ind].age = age
    return users[user_ind]


@app.delete('/user/{user_id}')
async def delete_user(
    user_id: Annotated[int, Path(ge=1, le=100, description='Введите id пользователя', example=1)]
) -> str:
    user_ind = get_user_index(user_id)
    users.pop(user_ind)
    return f'The user {user_id} has been deleted'

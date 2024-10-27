from fastapi import FastAPI, Path, HTTPException
from typing import Annotated, List
from pydantic import BaseModel

class User(BaseModel):
    id: int = None
    username: Annotated[str, Path(min_length=3, max_length=15, description='Введите имя пользователя',
                                  example='User')] = 'User'
    age: Annotated[int, Path(ge=18, le=120, description='Введите возраст', example=22)] = 22


app = FastAPI()
users: List[User] = []


def get_user_index(user_id: int):
    user_ind = None
    for i in range(len(users)):
        if users[i].id == user_id:
            user_ind = i
            break
    if user_ind is not None:
        return user_ind
    else:
        raise HTTPException(status_code=404, detail=f'User {user_id} was not found')


@app.get('/users')
async def get_users() -> List[User]:
    # print(users)
    return users


@app.post('/user/{username}/{age}')
async def add_user(user: User) -> str:
    user_id = users[-1].id + 1 if users != [] else 1
    user.id = user_id
    users.append(user)
    return f'User {user_id} is registered'


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
        user_id: Annotated[int, Path(ge=1, le=100, description='Введите id пользователя', example=1)],
        username: Annotated[
            str, Path(min_length=3, max_length=15, description='Введите имя пользователя', example='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=120, description='Введите возраст', example=25)]
) -> str:
    try:
        user_ind = get_user_index(user_id)
        users[user_ind].username = username
        users[user_ind].age = age
        return f'The user {user_id} has been updated'
    except HTTPException:
        raise


@app.delete('/user/{user_id}')
async def delete_user(
        user_id: Annotated[int, Path(ge=1, le=100, description='Введите id пользователя', example=1)]) -> str:
    try:
        user_ind = get_user_index(user_id)
        users.pop(user_ind)
        return f'The user {user_id} has been deleted'
    except HTTPException:
        raise
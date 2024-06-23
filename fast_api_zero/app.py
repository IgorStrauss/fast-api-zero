from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .schemas import Message, UserDB, UserList, UserPublic, UserSchema

database: list[UserDB] = []

app = FastAPI()


@app.get("/", response_model=Message, status_code=HTTPStatus.OK)
def read_root() -> dict:
    return {"message": "Olá Mundo!"}


@app.get("/path-html")
def read_html() -> HTMLResponse:
    html_content = """
    <html>
        <head>
            <title>MarquesIgor</title>
        </head>
        <body style="background-color:#1c1c1c;">
            <h1 style="color:red; text-align:center; margin-top:20rem">
            MarquesIgor
            </h1>
            <h1 style="color:red; text-align:center; margin-top:5rem">
            Curso FastAPI Zero com Dunossauro!
            </h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/users/", response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema) -> dict:

    user_with_id = UserDB(**user.model_dump(), Id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id


@app.get("/users/", response_model=UserList)
def read_users() -> dict:
    return {"users": database}


@app.get("/user/{user_id}", response_model=UserPublic)
def read_user(user_id: int) -> dict:
    if user_id > len(database) or user_id <= 0:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="User not found")
    return database[user_id - 1]


@app.put("/user/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserSchema) -> dict:
    if user_id > len(database) or user_id <= 0:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="User not found")
    user_with_id = UserDB(**user.model_dump(), Id=user_id)
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete("/user/{user_id}", response_model=Message)
def delete_user(user_id: int) -> dict:
    if user_id > len(database) or user_id <= 0:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="User not found")
    del database[user_id - 1]
    return {"message": "User deleted"}

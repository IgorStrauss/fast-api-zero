from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api_zero.database import get_session
from fast_api_zero.models import User
from fast_api_zero.schemas import Message, UserList, UserPublic, UserSchema

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
def create_user(
    user: UserSchema, session: Session = Depends(get_session)
) -> dict:
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Username already exists",
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Email already exists",
            )

    db_user = User(
        username=user.username, email=user.email, password=user.password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/users/", response_model=UserList)
def read_users(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
) -> dict:
    users = session.scalars(select(User).offset(skip).limit(limit)).all()

    return {"users": users}


@app.get("/user/{user_id}", response_model=UserPublic)
def read_user(user_id: int, session: Session = Depends(get_session)) -> dict:
    # sourcery skip: reintroduce-else, swap-if-else-branches, use-named-expression
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )
    return db_user


@app.put("/user/{user_id}", response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema,
    session: Session = Depends(get_session)
        ) -> dict:
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    session.commit()
    session.refresh(db_user)
    return db_user


@app.delete("/user/{user_id}", response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)) -> dict:
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )
    session.delete(db_user)
    session.commit()
    return {"message": "User deleted"}

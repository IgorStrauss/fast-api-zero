from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api_zero.database import get_session
from fast_api_zero.models import User
from fast_api_zero.schemas import (
    Message,
    Token,
    UserList,
    UserPublic,
    UserSchema,
)
from fast_api_zero.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

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


@app.post(
    "/users/",
    response_model=UserPublic,
    status_code=HTTPStatus.CREATED,
)
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
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get(
    "/users/",
    response_model=UserList,
)
def read_users(
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
) -> dict:
    users = session.scalars(select(User).offset(skip).limit(limit)).all()

    return {"users": users}


@app.get(
    "/user/{user_id}",
    response_model=UserPublic,
)
def read_user(
    user_id: int,
    session: Session = Depends(get_session),
) -> dict:
    if db_user := session.scalar(select(User).where(User.id == user_id)):
        return db_user
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )


@app.put(
    "/user/{user_id}",
    response_model=UserPublic,
)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
) -> dict:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permissions"
        )
    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)
    session.commit()
    session.refresh(current_user)
    return current_user


@app.delete("/user/{user_id}", response_model=Message)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
) -> dict:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permissions"
        )
    session.delete(current_user)
    session.commit()
    return {"message": "User deleted"}


@app.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    db_user = session.scalar(
        select(User).where(User.email == form_data.username)
    )
    if not db_user or not verify_password(
        form_data.password, db_user.password
    ):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": db_user.email})

    return {"access_token": access_token, "token_type": "Bearer"}

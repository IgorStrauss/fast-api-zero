from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api_zero.database import get_session
from fast_api_zero.models import User
from fast_api_zero.schemas import Message, UserList, UserPublic, UserSchema
from fast_api_zero.security import get_current_user, get_password_hash

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
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


@router.get(
    "/",
    response_model=UserList,
)
def read_users(
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
) -> dict:
    users = session.scalars(select(User).offset(skip).limit(limit)).all()

    return {"users": users}


@router.get(
    "/{user_id}",
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


@router.put(
    "/{user_id}",
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


@router.delete("/{user_id}", response_model=Message)
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

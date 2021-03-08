from sqlalchemy.orm import Session

from data.models import User
from data.schema.users import UserBase


def get_user(db: Session, user_id: int):
    return db.query(User).get(user_id)


def get_user_all(db: Session):
    return db.query(User).all()


def create_user(db: Session, user: UserBase):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(db: Session, user_id: int, user: UserBase):
    db.query(User).filter(User.id == user_id).update(
        user.dict(), synchronize_session='evaluate')
    db.commit()

    return get_user(db, user_id)


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)

    if not db_user:
        raise ValueError

    db.query(User).filter(User == db_user).delete(
        synchronize_session='evaluate')
    db.commit()

    return

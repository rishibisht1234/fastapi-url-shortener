from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.core.security import hash_password


def get_user_by_email(db: Session, email: str):
    statement = select(User).where(User.email == email)

    return db.scalar(statement)

def create_user(
        db:Session,
        email: str,
        password: str
):
    hashed_password = hash_password(password)

    new_user = User(email= email, hashed_password= hashed_password)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except IntegrityError:
        db.rollback()
        return None

    except Exception:
        db.rollback()
        raise
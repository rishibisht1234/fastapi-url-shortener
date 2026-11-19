from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.url import URL
from app.utils.short_code import generate_short_code

def create_short_url(db: Session, original_url: str, user_id: int):

    max_attempts = 5

    for attempt in range(max_attempts):

        short_code = generate_short_code()

        existing_url = db.scalar(
            select(URL).where(URL.short_code == short_code)
        )

        if existing_url:
            continue

        new_url = URL(
            original_url = original_url,
            short_code = short_code,
            user_id = user_id
        )

        try:
            db.add(new_url)
            db.commit()
            db.refresh(new_url)

            return new_url

        except IntegrityError:
            db.rollback()
            continue

        except Exception:
            db.rollback()
            raise

    raise RuntimeError(
        "Unable to generate a unique short code after multiple attempts"
    )


def get_all_urls(db: Session, user_id: int, limit: int = 10, skip: int = 0):
    
    statement = select(URL).where(URL.user_id==user_id).order_by(URL.id.desc()).limit(limit).offset(skip)
    return db.scalars(statement).all()


def get_url_by_id(db: Session, url_id: int, user_id: int):

    statement = select(URL).where( URL.id==url_id, URL.user_id==user_id)
    return db.scalar(statement)


def update_url(db: Session, url: URL, original_url: str):

    url.original_url = original_url

    try:
        db.commit()
        db.refresh(url)
        return url
    
    except Exception:
        db.rollback()
        raise

def delete_url(db: Session, url: URL):
    try:
        db.delete(url)
        db.commit()
    except Exception:
        db.rollback()
        raise


def get_url_by_code(db: Session, short_code: str):

    statement = select(URL).where(URL.short_code==short_code)

    return db.scalar(statement)



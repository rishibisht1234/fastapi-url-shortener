from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.url import URL
from app.utils.short_code import generate_short_code

def create_short_url(db: Session, original_url: str):

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
            short_code = short_code
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


def get_all_urls(db: Session, limit: int = 10, skip: int = 0):
    
    statement = select(URL).order_by(URL.id).limit(limit).offset(skip)
    return db.scalars(statement).all()


def get_url_by_id(db: Session, url_id: int):

    return db.get(URL, url_id)


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



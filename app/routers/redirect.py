from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database.connections import get_db
from app.services.url_service import get_url_by_code

router = APIRouter(tags=["Redirection"])

@router.get("/{short_code}")
def redirect_url(
    short_code: str,
    db: Session = Depends(get_db)
):
    url = get_url_by_code(db, short_code)

    if not url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    url.clicks += 1
    db.commit()

    return RedirectResponse(
        url=url.original_url,
        status_code=302
    )
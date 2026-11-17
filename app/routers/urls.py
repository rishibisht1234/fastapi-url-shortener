from fastapi import Query, APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.connections import get_db
from app.models.url import URL
from app.schemas.url import URLCreate, URLUpdate, URLResponse
from app.services.url_service import (
    create_short_url,
    get_all_urls,
    get_url_by_code,
    get_url_by_id,
    update_url as update_url_service,
    delete_url as delete_url_service
)
from app.core.config import settings

router = APIRouter(
    prefix='/urls',
    tags = ['URLs']
)

    

@router.post(
    "/",
    response_model=URLResponse,
    status_code=status.HTTP_201_CREATED         
    )
def create_url(
    url_data: URLCreate,
    db: Session = Depends(get_db)
):
    new_url = create_short_url(
        db = db,
        original_url= str(url_data.original_url)
    )

    return new_url



@router.get("/", response_model=list[URLResponse])
def get_urls(
    limit: int = Query(default=10, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)):

    urls = get_all_urls(db, limit, skip)

    return urls



@router.get("/{url_id}", response_model= URLResponse)
def get_url(url_id: int, db: Session = Depends(get_db)):
    
    url = get_url_by_id(db, url_id)

    if not url:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "URL not found"
        )

    return url



@router.patch("/{url_id}", response_model=URLResponse)
def update_url(
    url_id : int,
    url_data : URLUpdate,
    db: Session = Depends(get_db)
):
    url = get_url_by_id(db, url_id)

    if not url:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "URL not found"
        )

    update_data = url_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = 'no fields provided for update'
        )

    if update_data.get('original_url') is None:
        raise HTTPException(
            status_code=422,
            detail= 'Original URL cannot be null'
        )

    return update_url_service(db, url, str(update_data.get('original_url')))
    
    

@router.delete("/{url_id}", status_code= 204)
def delete_url(
    url_id: int,
    db: Session = Depends(get_db)
):
    url = get_url_by_id(db, url_id)

    if not url:
        raise HTTPException(
            status_code=404,
            detail='URL not found'
        )

    delete_url_service(db, url)

    return Response(status_code=204)




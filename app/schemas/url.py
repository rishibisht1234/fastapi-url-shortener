from pydantic import BaseModel, HttpUrl, ConfigDict, computed_field
from datetime import datetime
from app.core.config import settings

class URLCreate(BaseModel):
    original_url: HttpUrl


class URLUpdate(BaseModel):
    original_url : HttpUrl | None = None


class URLResponse(BaseModel):
    id : int
    original_url : str
    short_code : str
    # short_url: str
    clicks: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def short_url(self)->str:
        return f'{settings.BASE_URL}/{self.short_code}'
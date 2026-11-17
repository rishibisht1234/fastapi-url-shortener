from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.database.connections import Base

class URL(Base):

    __tablename__ = 'urls'

    id : Mapped[int] = mapped_column(primary_key=True)

    original_url : Mapped[str] = mapped_column(String(2048), nullable=False)
    short_code : Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    clicks : Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                  server_default=func.now(),
                                                  nullable=False
                                                  )
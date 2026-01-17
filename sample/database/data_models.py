from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass,
    mapped_column,
    Mapped
)
from sqlalchemy import (
    String,
    Integer,
)


class Base(AsyncAttrs, DeclarativeBase, MappedAsDataclass):
    pass

class VolumeDB(Base):
    __tablename__ = "volumes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    size: Mapped[int] = mapped_column(Integer)

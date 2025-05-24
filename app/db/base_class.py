import re

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql import func


@as_declarative()  # This is key!
class Base:
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    @declared_attr
    def __tablename__(cls) -> str:
        name = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
        if name.endswith("y"):
            name = name[:-1] + "ies"
        elif not name.endswith("s"):
            name += "s"
        return name

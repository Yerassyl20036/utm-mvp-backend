# backend/app/db/base_class.py
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, Integer
import re

# REMOVE THE MODEL IMPORTS FROM HERE:
# from app.models.organization import Organization # noqa
# from app.models.pilot import Pilot # noqa
# Add other models as they are created

@as_declarative()
class Base:
    """
    Base class which provides automated table name
    and surrogate primary key column.
    """

    @declared_attr
    def __tablename__(cls) -> str:
        # Converts CamelCase class names to snake_case table names
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower() + "s" # Pluralize

    id = Column(Integer, primary_key=True, index=True)
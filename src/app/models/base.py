from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from app.utils.case_converter import camel_case_to_snake_case
from app.utils.naming import NAMING_CONVENTION


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=NAMING_CONVENTION,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Generate table name from class name in snake_case."""
        name = camel_case_to_snake_case(cls.__name__)
        return name if name.endswith("s") else f"{name}s"

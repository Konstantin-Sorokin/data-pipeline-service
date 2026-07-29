from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.file import File


class Calculation(Base):
    id: Mapped[int] = mapped_column(primary_key=True)

    file_id: Mapped[int] = mapped_column(
        ForeignKey("files.id"),
        unique=True,
        nullable=False,
    )
    digit_0_count: Mapped[int] = mapped_column(Integer, nullable=False)
    digit_1_count: Mapped[int] = mapped_column(Integer, nullable=False)
    digit_2_count: Mapped[int] = mapped_column(Integer, nullable=False)
    digit_3_count: Mapped[int] = mapped_column(Integer, nullable=False)
    digit_4_count: Mapped[int] = mapped_column(Integer, nullable=False)
    digit_5_count: Mapped[int] = mapped_column(Integer, nullable=False)
    digit_6_count: Mapped[int] = mapped_column(Integer, nullable=False)
    digit_7_count: Mapped[int] = mapped_column(Integer, nullable=False)
    digit_8_count: Mapped[int] = mapped_column(Integer, nullable=False)
    digit_9_count: Mapped[int] = mapped_column(Integer, nullable=False)

    file: Mapped["File"] = relationship(back_populates="calculation")

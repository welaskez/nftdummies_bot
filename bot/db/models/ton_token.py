from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class TonToken(Base):
    ticker: Mapped[str] = mapped_column(unique=True)
    jetton_master_address: Mapped[str] = mapped_column(unique=True)
    sticker_file_id: Mapped[str] = mapped_column(unique=True)

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import BigInteger, DateTime, func


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


class TonToken(Base):
    ticker: Mapped[str] = mapped_column(unique=True)
    jetton_master_address: Mapped[str] = mapped_column(unique=True)
    sticker_file_id: Mapped[str] = mapped_column(unique=True)


class User(Base):
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)

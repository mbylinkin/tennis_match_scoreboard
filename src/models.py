import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from src import constants


class Base(DeclarativeBase):
    metadata = sa.MetaData(naming_convention=constants.DB_NAMING_CONVENTION)

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self) -> str:
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class Player(Base):
    __tablename__ = "player"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(sa.String(250), unique=True)


class Match(Base):
    __tablename__ = "match"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    uuid: Mapped[str] = mapped_column(sa.String(32), unique=True)
    player1_id: Mapped[int] = mapped_column(sa.ForeignKey("player.id"))
    player2_id: Mapped[int] = mapped_column(sa.ForeignKey("player.id"))
    winner_id: Mapped[int] = mapped_column(sa.ForeignKey("player.id"))
    score: Mapped[str] = mapped_column(sa.String(500))

    player1: Mapped["Player"] = relationship(
        foreign_keys=[player1_id], lazy="joined", innerjoin=True
    )
    player2: Mapped["Player"] = relationship(
        foreign_keys=[player2_id], lazy="joined", innerjoin=True
    )
    winner: Mapped["Player"] = relationship(
        foreign_keys=[winner_id], lazy="joined", innerjoin=True
    )

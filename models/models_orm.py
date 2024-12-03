from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import String


class Base(DeclarativeBase):
    pass


class UserOrm(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column()
    memory_limit: Mapped[int] = mapped_column(default=1024 ** 2)
    memory_usage: Mapped[int] = mapped_column(default=0)
    # role: Mapped[str] = # TODO: enum for roles

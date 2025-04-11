"""Turso query and connection management module"""

import logging
from os import environ

from dotenv import load_dotenv
from sqlalchemy import LargeBinary, create_engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM"""

    pass


class Entry(Base):
    """Base database entry class"""

    __tablename__ = "urls"
    hashsum: Mapped[str] = mapped_column(primary_key=True)
    url: Mapped[bytes] = mapped_column(LargeBinary)
    salt: Mapped[bytes] = mapped_column(LargeBinary)

    def __repr__(self) -> str:
        return f"entry(hashsum={self.hashsum!r}, url={self.url!r}, salt={self.salt!r})"


load_dotenv()

# Get environment variables
TURSO_DATABASE_URL = environ["ENDPOINT"]
TURSO_AUTH_TOKEN = environ["TOKEN"]

# construct SQLAlchemy URL
DBURL = f"sqlite+{TURSO_DATABASE_URL}/?authToken={TURSO_AUTH_TOKEN}&secure=true"

engine = create_engine(
    DBURL,
    hide_parameters=True,
    connect_args={"check_same_thread": True},
    echo=True,
)


def get_link(hashsum: str):
    """Get entries that match provided path, return output string or bool False if fail"""
    try:
        session = Session(engine)
        # Get items
        stmt = select(Entry).where(Entry.hashsum.in_([hashsum]))
        for item in session.scalars(stmt):
            url = bytes(item.url)
            salt = bytes(item.salt)
        return url, salt
    except Exception as e:
        logging.error("Error on get_link: %s", e)
        return False


def insert_link(hashsum: str, url: bytes, salt: bytes):
    """Insert an entry under the specified path, return bool outcome"""
    try:
        with Session(engine) as session:
            # Insert entry
            new_entry = Entry(hashsum=str(hashsum), url=bytes(url), salt=bytes(salt))
            session.add(new_entry)
            session.commit()
            return True
    except Exception as e:
        logging.error("Error on insert_link:  %s", e)
        return False


def check_link(hashsum: str):
    """Return if an entry exists under specified path"""
    try:
        session = Session(engine)
        # Return if entry exists
        return bool(session.query(Entry).filter_by(hashsum=hashsum).first())
    except Exception as e:
        logging.error("Error on check_link:  %s", e)
        return False

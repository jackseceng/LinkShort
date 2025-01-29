"""Turso query and connection management module"""

import logging
from os import environ

from dotenv import load_dotenv
from sqlalchemy import String, create_engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Entry(Base):
    """Base database entry class"""

    __tablename__ = "links"
    path: Mapped[str] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"entry(path={self.path!r}, link={self.link!r})"


load_dotenv()

# Get environment variables
TURSO_DATABASE_URL = environ["ENDPOINT"]
TURSO_AUTH_TOKEN = environ["TOKEN"]

# construct SQLAlchemy URL
dbUrl = f"sqlite+{TURSO_DATABASE_URL}/?authToken={TURSO_AUTH_TOKEN}&secure=true"

engine = create_engine(
    dbUrl,
    pool_pre_ping=True,
    hide_parameters=True,
    connect_args={"check_same_thread": False},
    echo=True
)


def get_link(path):
    """Get entries that match provided path, return output string or bool False if fail"""
    try:
        session = Session(engine)
        # Get items
        stmt = select(Entry).where(Entry.path.in_([path]))
        for item in session.scalars(stmt):
            output = item.link
        return output
    except SQLAlchemyError as e:
        logging.error("Error on get_link: %s", e)
        return False


def insert_link(path, link):
    """Insert an entry under the specified path, return bool outcome"""
    try:
        with Session(engine) as session:
            print(path, link)
            # Insert entry
            new_entry = Entry(path=str(path), link=str(link))
            session.add(new_entry)
            session.commit()
            return True
    except SQLAlchemyError as e:
        logging.error("Error on insert_link:  %s", e)
        return False


def check_link(path):
    """Return if an entry exists under specified path"""
    try:
        session = Session(engine)
        # Return if entry exists
        return bool(session.query(Entry).filter_by(path=path).first())
    except SQLAlchemyError as e:
        logging.error("Error on check_link:  %s", e)
        return False

"""Turso query and connection management module"""

from os import environ
from dotenv import load_dotenv

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError


class Base(DeclarativeBase):
    pass


class Entry(Base):
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
    dbUrl, connect_args={"check_same_thread": False}, echo=False, hide_parameters=True
)


def get_link(path):
    try:
        session = Session(engine)
        # Get items
        stmt = select(Entry).where(Entry.path.in_([path]))
        for item in session.scalars(stmt):
            output = item.link
        return output
    except SQLAlchemyError as e:
        print(f"Error on get_link: {e}")
        return False


def insert_link(path, link):
    try:
        with Session(engine) as session:
            print(path, link)
            # Insert entry
            new_entry = Entry(path=str(path), link=str(link))
            session.add(new_entry)
            session.commit()
            return True
    except SQLAlchemyError as e:
        print(f"Error on insert_link: {e}")
        return False


def check_link(path):
    try:
        session = Session(engine)
        # Return if entry exists
        return bool(session.query(Entry).filter_by(path=path).first())
    except SQLAlchemyError as e:
        print(f"Error on check_link: {e}")
        return False

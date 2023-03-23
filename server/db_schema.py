# import sqlalchemy as db

import enum

from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, Integer, String, UniqueConstraint, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql.sqltypes import Boolean

from config.constants import DB_CREDENTIALS

DATABASE_URI = "postgresql://{}:{}@{}/{}".format(
    DB_CREDENTIALS["USERNAME"], DB_CREDENTIALS["PASSWORD"], DB_CREDENTIALS["HOSTNAME"], DB_CREDENTIALS["DB_NAME"],
)

ssl_args = {
    "sslrootcert": DB_CREDENTIALS["SSLROOTCERT"],
    "sslcert": DB_CREDENTIALS["SSLCERT"],
    "sslkey": DB_CREDENTIALS["SSLKEY"],
}
db_engine = create_engine(DATABASE_URI, connect_args=ssl_args, pool_pre_ping=True)
db_declarative_base = declarative_base()
session = sessionmaker(db_engine)
db_session = session()

# autouser - Default user for all updates from script

class Users(db_declarative_base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    email_id = Column(String(64), nullable=False)
    role = Column(Integer, ForeignKey("role.id"))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_by = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    created_by = Column(String(64), nullable=False)


class Role(db_declarative_base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_by = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    created_by = Column(String(64), nullable=False)
    users = relationship("Users")


def recreate_database():
    db_declarative_base.metadata.drop_all(db_engine)
    db_declarative_base.metadata.create_all(db_engine)

if __name__ == "__main__":
    recreate_database()

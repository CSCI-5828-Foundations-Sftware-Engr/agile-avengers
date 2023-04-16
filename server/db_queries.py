import sqlalchemy
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import aliased
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import exists
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from config.constants import DB_CREDENTIALS



# connecting to postgres database
DATABASE_URI = "postgresql://{}:{}@{}/{}".format(
    DB_CREDENTIALS["USERNAME"],
    DB_CREDENTIALS["PASSWORD"],
    DB_CREDENTIALS["HOSTNAME"],
    DB_CREDENTIALS["DB_NAME"],
)
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

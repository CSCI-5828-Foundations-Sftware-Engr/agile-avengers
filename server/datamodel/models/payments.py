import os, sys
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, FLOAT

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "."))
from userinfo import UserInfo

Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transaction"

    transaction_id = Column(Integer, autoincrement=True, primary_key=True)
    payer_id = Column(Integer, ForeignKey(UserInfo.user_id))
    payee_id = Column(Integer, ForeignKey(UserInfo.user_id))
    transaction_amount = Column(FLOAT())
    transaction_method = Column(String(30))
    transaction_method_id = Column(String(30))
    is_completed = Column(Boolean)
    created_on = Column(DateTime)
    created_by = Column(String(30))
    updated_on = Column(DateTime)
    updated_by = Column(String(30))

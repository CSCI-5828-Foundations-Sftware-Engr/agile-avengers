from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, DOUBLE

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transaction"

    transaction_id = Column(Integer, autoincrement=True, primary_key=True)
    payer_id = Column(String(30), ForeignKey("user_info.user_id"))
    payee_id = Column(String(30), ForeignKey("user_info.user_id"))
    transaction_amount = Column(DOUBLE(precision=64))
    transaction_method = Column(String(30))
    is_completed = Column(Boolean)
    created_on = Column(DateTime)
    created_by = Column(String(30))
    updated_on = Column(DateTime)
    updated_by = Column(String(30))

class RequestedPayments(Base):
    __tablename__ = "requested_payments"

    transaction_id = Column(Integer, ForeignKey("transaction.transaction_id"))
    payer_id = Column(String(30), ForeignKey("user_info.user_id"))
    payee_id = Column(String(30), ForeignKey("user_info.user_id"))
    is_pending = Column(Boolean)
    amount_requested = Column(DOUBLE(precision=64))
    
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    FLOAT,
    create_engine,
)
from config import DB_USERNAME, DB_HOSTNAME, DB_PASSWORD, DB_NAME

Base = declarative_base()


class UserInfo(Base):
    __tablename__ = "user_info"

    user_id = Column(Integer, autoincrement=True, primary_key=True)
    user_name = Column(String(30), unique=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    mobile_number = Column(String(10))
    email_id = Column(String(30))
    is_merchant = Column(Boolean)
    created_on = Column(DateTime)
    created_by = Column(String(30))
    updated_on = Column(DateTime)
    updated_by = Column(String(30))


class BankAccount(Base):
    __tablename__ = "bank_account"

    account_number = Column(String(30), primary_key=True)
    user_id = Column(Integer, ForeignKey("user_info.user_id"))
    account_holders_name = Column(String(30))
    account_balance = Column(FLOAT())
    bank_name = Column(String(30))
    routing_number = Column(String(30))
    created_on = Column(DateTime)
    created_by = Column(String(30))
    updated_on = Column(DateTime)
    updated_by = Column(String(30))


class BillingInfo(Base):
    __tablename__ = "billing_info"

    billing_info_id = Column(Integer, autoincrement=True, primary_key=True)
    billing_address = Column(String(70))
    postal_code = Column(String(8))
    state = Column(String(30))
    city = Column(String(30))


class DebitCard(Base):
    __tablename__ = "debit_card"

    card_number = Column(String(16), primary_key=True)
    user_id = Column(Integer, ForeignKey("user_info.user_id"))
    card_network = Column(String(30))
    cvv = Column(String(30))
    billing_info_id = Column(Integer, ForeignKey("billing_info.billing_info_id"))
    bank_account_number = Column(String(30), ForeignKey("bank_account.account_number"))
    created_on = Column(DateTime)
    created_by = Column(String(30))
    updated_on = Column(DateTime)
    updated_by = Column(String(30))


class CreditCard(Base):
    __tablename__ = "credit_card"

    card_number = Column(String(16), primary_key=True)
    user_id = Column(Integer, ForeignKey("user_info.user_id"))
    card_network = Column(String(30))
    cvv = Column(String(30))
    billing_info_id = Column(Integer, ForeignKey("billing_info.billing_info_id"))
    credit_limit = Column(FLOAT())
    created_on = Column(DateTime)
    created_by = Column(String(30))
    updated_on = Column(DateTime)
    updated_by = Column(String(30))


class Merchant(Base):
    __tablename__ = "merchant"
    merchant_id = Column(Integer, autoincrement=True, primary_key=True)
    merchant_name = Column(String)
    category = Column(String)
    sub_category = Column(String)
    user_id = Column(Integer, ForeignKey("user_info.user_id"))


class Transaction(Base):
    __tablename__ = "transaction"

    transaction_id = Column(Integer, autoincrement=True, primary_key=True)
    payer_id = Column(Integer, ForeignKey(UserInfo.user_id))
    payee_id = Column(Integer, ForeignKey(UserInfo.user_id))
    transaction_amount = Column(FLOAT())
    transaction_method = Column(String(30))
    transaction_method_id = Column(String(30))
    merchant_id = Column(Integer, ForeignKey(Merchant.merchant_id))
    is_completed = Column(Boolean)
    created_on = Column(DateTime)
    created_by = Column(String(30))
    updated_on = Column(DateTime)
    updated_by = Column(String(30))


DATABASE_URI = "postgresql://{}:{}@{}/{}".format(
    DB_USERNAME, DB_PASSWORD, DB_HOSTNAME, DB_NAME
)
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

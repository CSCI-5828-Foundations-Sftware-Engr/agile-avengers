from datamodel import session, UserInfo, Transaction, Merchant
import sqlalchemy


def user_exists(user_id):
    user = session.query(UserInfo).filter_by(user_id=user_id).first()
    if user:
        return True
    return False


def summarize_category(user_id, on="category"):
    if on == "category":
        result = {}
        query = (
            session.query(
                Merchant.category, sqlalchemy.func.sum(Transaction.transaction_amount).label("total")
            )
            .join(Merchant, Transaction.merchant_id==Merchant.merchant_id)
            .filter(Transaction.payer_id==user_id)
            .group_by(Merchant.category)
        )
        for row in query.all():
            result[row.category] = row.total
        return result

    if on == "sub_category":
        result = {}
        query = (
            session.query(
                Merchant.sub_category,
                sqlalchemy.func.sum(Transaction.transaction_amount).label("total"),
            )
            .join(Merchant, Transaction.merchant_id == Merchant.merchant_id)
            .filter(Transaction.payer_id==user_id)
            .group_by(Merchant.sub_category)
        )
        for row in query.all():
            result[row.sub_category] = row.total
        return result

    if on == "merchant":
        result = {}
        query = (
            session.query(
                Merchant.merchant_name,
                sqlalchemy.func.sum(Transaction.transaction_amount).label("total"),
            )
            .join(Merchant, Transaction.merchant_id == Merchant.merchant_id)
            .filter(Transaction.payer_id==user_id)
            .group_by(Merchant.merchant_name)
        )
        for row in query.all():
            result[row.merchant_name] = row.total
        return result

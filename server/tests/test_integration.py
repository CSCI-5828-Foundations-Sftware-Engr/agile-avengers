import sys
from unittest.mock import Mock
sys.modules['helpers.user_management'] = Mock()

from datetime import datetime
from unittest import mock

from datamodel.models.userinfo import BankAccount, Base, BillingInfo, CreditCard, DebitCard, UserInfo
from datamodel.models.payments import Transaction
from db_queries import engine, session
from flask_app import app


class TestIntegration:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = session
        self.app_client = app.test_client()
        self.payee_id=None
        self.user_data = {
            "user_name": "aditi",
            "first_name": "Aditi",
            "last_name": "Athreya",
            "mobile_number": "1234566789",
            "email_id": "adra9557@colorado.edu",
            "is_merchant": False,
            "created_by": "aditi",
            "updated_by": "aditi",
        }
        self.bankaccount_data = {
            "account_number": "123456789123",
            "user_id": "1",
            "account_holders_name": "Aditi Athreya",
            "account_balance": "1000",
            "bank_name": "Chase",
            "routing_number": "987654321",
            "created_by": "aditi",
            "updated_by": "aditi",
        }

    def teardown_class(self):
        self.session.rollback()
        self.session.close()


    def create_payee(self):
        payee = UserInfo(
            user_name="preetham",
            first_name="Preetham",
            last_name="Maiya",
            mobile_number="1234566789",
            email_id="prma6536@colorado.edu",
            is_merchant=False,
            created_on=datetime.now(),
            created_by="preetham",
            updated_on=datetime.now(),
            updated_by="preetham",
        )

        self.session.add(payee)
        self.session.commit()

        self.payee_id=payee.user_id



    def create_payee_bank_account(self):
        # payee account
        payee_ba = BankAccount(
            account_number="123456789123423567",
            user_id=self.payee_id,
            account_holders_name="Preetham Maiya",
            account_balance=5000,
            bank_name="Chase",
            routing_number="122357247",
        )

        self.session.add(payee_ba)
        self.session.commit()    


    
    @mock.patch("flask_app.user_login")
    @mock.patch("flask_app.create_new_user")
    def test_signup_sendpayment(self, mock_create_new_user,mock_user_login):
        signup_url = "/v1/auth/create"
        createaccount_url = "/v1/users/create"
        login_url = "/v1/auth/login"
        create_bankaccount_url="/v1/bankaccount/add"
        send_url = "/v1/payment/send"
        data = {"username": "aditi", "password": "password"}

        # Happy path
        #Sign Up to Easy Pay
        mock_create_new_user.return_value = data
        res = self.app_client.post(signup_url, json=data, follow_redirects=True)
        assert res.status_code == 200

        users = (
            self.session.query(UserInfo).filter(UserInfo.user_name == "aditi").all()
        )
        assert len(users) == 1


        #Create Account in EasyPay
        res = self.app_client.post(createaccount_url, json=self.user_data)

        assert res.status_code == 200

        users = (
            self.session.query(UserInfo).filter(UserInfo.user_name == "aditi").all()
        )
        assert len(users) == 1
        assert users[0].user_name == "aditi"
        assert users[0].first_name == "Aditi"
        assert users[0].last_name == "Athreya"
        assert users[0].mobile_number == "1234566789"
        assert users[0].email_id == "adra9557@colorado.edu"
        assert users[0].is_merchant == False
        assert users[0].created_by == "aditi"
        assert users[0].updated_by == "aditi"


        #Login to EasyPay
        mock_user_login.return_value = {"access_token": "1", "refersh_token": "2"}
        res = self.app_client.post(login_url, json=data)
        assert res.status_code == 200

        #Add bank account details in EasyPay
        self.bankaccount_data["user_id"]=users[0].user_id
        res = self.app_client.post(create_bankaccount_url, json=self.bankaccount_data)
        assert res.status_code == 200

        cards = (
            self.session.query(BankAccount)
            .filter(BankAccount.account_number == "123456789123")
            .all()
        )
        assert len(cards) == 1
        assert cards[0].user_id == users[0].user_id
        assert cards[0].account_number == "123456789123"
        assert cards[0].account_holders_name == "Aditi Athreya"
        assert cards[0].bank_name == "Chase"
        assert cards[0].routing_number == "987654321"
        assert cards[0].created_by == str(users[0].user_id)
        assert cards[0].updated_by == str(users[0].user_id)


        #Sending payment
        self.create_payee()
        self.create_payee_bank_account()
        req = {
            "payer_id": users[0].user_id,
            "payee_id": self.payee_id,
            "transaction_amount": 100,
            "transaction_method": "bank",
            "transaction_method_id": "123456789123",
        }
        res = self.app_client.post(send_url, json=req)
        assert res.status_code == 201
        cards = (
            self.session.query(BankAccount)
            .filter(BankAccount.account_number == "123456789123423567")
            .all()
        )
        assert cards[0].account_balance == 5100
        transaction_id = res.json["id"]


        # Cleanup
        self.session.query(Transaction).filter(
            Transaction.transaction_id == transaction_id
        ).delete()

        self.session.query(BankAccount).filter(
            BankAccount.account_number == "123456789123"
        ).delete()
        self.session.commit()

        self.session.query(BankAccount).filter(
            BankAccount.account_number == "123456789123423567"
        ).delete()
        self.session.commit()

        self.session.query(UserInfo).filter(UserInfo.user_name == "aditi").delete()
        self.session.commit()

        self.session.query(UserInfo).filter(UserInfo.user_name == "preetham").delete()
        self.session.commit()

       
        

    @mock.patch("flask_app.user_login")
    @mock.patch("flask_app.create_new_user")
    def test_signup_requestpayment(self, mock_create_new_user,mock_user_login):
        signup_url = "/v1/auth/create"
        createaccount_url = "/v1/users/create"
        login_url = "/v1/auth/login"
        create_bankaccount_url="/v1/bankaccount/add"
        request_url = "/v1/payment/request"
        data = {"username": "aditi", "password": "password"}

        # Happy path
        #Sign Up to Easy Pay
        mock_create_new_user.return_value = data
        res = self.app_client.post(signup_url, json=data, follow_redirects=True)
        assert res.status_code == 200

        users = (
            self.session.query(UserInfo).filter(UserInfo.user_name == "aditi").all()
        )
        assert len(users) == 1


        #Create Account in EasyPay
        res = self.app_client.post(createaccount_url, json=self.user_data)

        assert res.status_code == 200

        users = (
            self.session.query(UserInfo).filter(UserInfo.user_name == "aditi").all()
        )
        assert len(users) == 1
        assert users[0].user_name == "aditi"
        assert users[0].first_name == "Aditi"
        assert users[0].last_name == "Athreya"
        assert users[0].mobile_number == "1234566789"
        assert users[0].email_id == "adra9557@colorado.edu"
        assert users[0].is_merchant == False
        assert users[0].created_by == "aditi"
        assert users[0].updated_by == "aditi"


        #Login to EasyPay
        mock_user_login.return_value = {"access_token": "1", "refersh_token": "2"}
        res = self.app_client.post(login_url, json=data)
        assert res.status_code == 200

        #Add bank account details in EasyPay
        self.bankaccount_data["user_id"]=users[0].user_id
        res = self.app_client.post(create_bankaccount_url, json=self.bankaccount_data)
        assert res.status_code == 200

        cards = (
            self.session.query(BankAccount)
            .filter(BankAccount.account_number == "123456789123")
            .all()
        )
        assert len(cards) == 1
        assert cards[0].user_id == users[0].user_id
        assert cards[0].account_number == "123456789123"
        assert cards[0].account_holders_name == "Aditi Athreya"
        assert cards[0].bank_name == "Chase"
        assert cards[0].routing_number == "987654321"
        assert cards[0].created_by == str(users[0].user_id)
        assert cards[0].updated_by == str(users[0].user_id)


        #Requesting payment
        self.create_payee()
        self.create_payee_bank_account()
        req = {
            "requestor_id": self.payee_id,
            "sender_id": users[0].user_id,
            "transaction_amount": 100,
        }
        res = self.app_client.post(request_url, json=req)
        assert res.status_code == 201
        transaction_id = res.json["id"]
        transaction = (
            self.session.query(Transaction)
            .filter(Transaction.transaction_id == transaction_id)
            .first()
        )
        assert transaction != None  # check if transaction is created
        assert transaction.is_completed == False


        # Cleanup
        self.session.query(Transaction).filter(
            Transaction.transaction_id == transaction_id
        ).delete()

        self.session.query(BankAccount).filter(
            BankAccount.account_number == "123456789123"
        ).delete()
        self.session.commit()

        self.session.query(BankAccount).filter(
            BankAccount.account_number == "123456789123423567"
        ).delete()
        self.session.commit()

        self.session.query(UserInfo).filter(UserInfo.user_name == "aditi").delete()
        self.session.commit()

        self.session.query(UserInfo).filter(UserInfo.user_name == "preetham").delete()
        self.session.commit()

       
from datamodel.models.userinfo import Base, UserInfo, CreditCard, DebitCard, BankAccount
from datamodel.models.payments import Transaction
from db_queries import session, engine
from flask_app import app
from unittest import mock
from datetime import datetime

class TestPayment:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = session
        self.app_client = app.test_client()
        self.payer_data = {
            "user_name": "preetham",
            "first_name": "Preetham",
            "last_name": "Maiya",
            "mobile_number": "1234566789",
            "email_id": "prma6536@colorado.edu",
            "is_merchant": False,
            "created_by": "preetham",
            "updated_by": "preetham",
        }
        self.payee_data = {
            "user_name": "ashutosh",
            "first_name": "Ashutosh",
            "last_name": "Gandhi",
            "mobile_number": "1234566289",
            "email_id": "asga5889@colorado.edu",
            "is_merchant": False,
            "created_by": "ashutosh",
            "updated_by": "ashutosh",
        }
        self.payer_id = None
        self.payee_id = None
        self.base_url = "/v1/payment"

    def teardown_class(self):
        self.session.rollback()
        self.session.close()
    
    def create_payer_payee_user(self):
        payer = UserInfo(
            # user_id = 1, # @TODO this id may already exists
            user_name = self.payer_data["user_name"],
            first_name = self.payer_data["first_name"],
            last_name = self.payer_data["last_name"],
            mobile_number = self.payer_data["mobile_number"],
            email_id = self.payer_data["email_id"],
            is_merchant = self.payer_data["is_merchant"],
            created_on = datetime.now(),
            created_by = self.payer_data["created_by"],
            updated_on = datetime.now(),
            updated_by = self.payer_data["updated_by"],
        )

        payee = UserInfo(
            # user_id = 2,
            user_name = self.payee_data["user_name"],
            first_name = self.payee_data["first_name"],
            last_name = self.payee_data["last_name"],
            mobile_number = self.payee_data["mobile_number"],
            email_id = self.payee_data["email_id"],
            is_merchant = self.payee_data["is_merchant"],
            created_on = datetime.now(),
            created_by = self.payee_data["created_by"],
            updated_on = datetime.now(),
            updated_by = self.payee_data["updated_by"],
        )

        self.session.add(payer)
        self.session.add(payee)
        self.session.commit()

        self.payer_id = payer.user_id
        self.payee_id = payee.user_id
    
    def create_credit_card(self, limit):
        card = CreditCard(
            card_number="1234567891234568",
            user_id=self.payer_id,
            card_network="Visa",
            cvv="333",
            credit_limit=limit
        )
        self.session.add(card)
        self.session.commit()
    
    def create_debit_card(self):
        card = DebitCard(
            user_id=self.payer_id,
            card_number="1234567891234567",
            card_network="Visa",
            cvv="222",
            bank_account_number="123456789123423567"
        )
        self.session.add(card)
        self.session.commit()
    
    def create_bank_account(self, balance):
        # payer account
        payer = BankAccount(
            account_number = "123456789123423567",
            user_id = self.payer_id,
            account_holders_name = "Preetham Maiya",
            account_balance = balance,
            bank_name = "Chase",
            routing_number = "122357247"
        )

        # payee account 
        payee = BankAccount(
            account_number = "1234562315423567",
            user_id = self.payee_id,
            account_holders_name = "Ashutosh Gandhi",
            account_balance = 5000,
            bank_name = "Chase",
            routing_number = "122357247"
        )

        self.session.add(payer)
        self.session.add(payee)
        self.session.commit()
    

    def cleanup_entires(self):

        # delete credit card
        self.session.query(CreditCard).filter(CreditCard.card_number == "1234567891234568").delete()
        # delete debit card
        self.session.query(DebitCard).filter(DebitCard.card_number == "1234567891234567").delete()
        # delete bank account
        self.session.query(BankAccount).filter(BankAccount.account_number.in_(["1234562315423567", "123456789123423567"])).delete()
        # delete payer and payee info
        self.session.query(UserInfo).filter(UserInfo.user_id.in_([self.payer_id, self.payee_id])).delete()

        self.session.commit()
    

    def assert_balance(self, res, method):
        assert res.status_code == 201

        user = self.session.query(BankAccount).filter(BankAccount.account_number == "1234562315423567").first()
        assert user.account_balance == 5100 # payee balance increased
        
        if method == "credit":
            credit = self.session.query(CreditCard).filter(CreditCard.card_number == "1234567891234568").first()
            assert credit.credit_limit == 1900
        else:
            user = self.session.query(BankAccount).filter(BankAccount.account_number == "123456789123423567").first()
            assert user.account_balance == 9900 # payer balance decreased


    def test_send_bank_transaction(self):
        url = f"{self.base_url}/send"

        # create users and bank accounts
        self.create_payer_payee_user()
        self.create_bank_account(10000)

        req = {
            "payer_id": self.payer_id,
            "payee_id": self.payee_id,
            "transaction_amount": 100,
            "transaction_method": "bank",
            "transaction_method_id": "123456789123423567"
        }

        res = self.app_client.post(url, json=req)
        
        self.assert_balance(res, "bank")

        transaction_id = res.json["id"]
        # cleanup
        self.session.query(Transaction).filter(Transaction.transaction_id == transaction_id).delete()
        self.cleanup_entires()
    

    def test_send_debit_transaction(self):
        url = f"{self.base_url}/send"

        # create users and bank accounts and debit card
        self.create_payer_payee_user()
        self.create_bank_account(10000)
        self.create_debit_card()

        req = {
            "payer_id": self.payer_id,
            "payee_id": self.payee_id,
            "transaction_amount": 100,
            "transaction_method": "debit",
            "transaction_method_id": "1234567891234567"
        }

        res = self.app_client.post(url, json=req)
        
        self.assert_balance(res, "debit")
       
        transaction_id = res.json["id"] 
        # cleanup
        self.session.query(Transaction).filter(Transaction.transaction_id == transaction_id).delete()
        self.cleanup_entires()
    

    def test_send_credit_transaction(self):
        url = f"{self.base_url}/send"

        # create users and bank accounts and credit card
        self.create_payer_payee_user()
        self.create_bank_account(10000)
        self.create_credit_card(2000)

        req = {
            "payer_id": self.payer_id,
            "payee_id": self.payee_id,
            "transaction_amount": 100,
            "transaction_method": "credit",
            "transaction_method_id": "1234567891234568"
        }

        res = self.app_client.post(url, json=req)
        
        self.assert_balance(res, "credit")
       
        transaction_id = res.json["id"] 
        # cleanup
        self.session.query(Transaction).filter(Transaction.transaction_id == transaction_id).delete()
        self.cleanup_entires()
    
    def test_payee_list(self):
        url = f"{self.base_url}/get_payee_list"
        # create users
        self.create_payer_payee_user()

        res = self.app_client.get(url)
        assert res.status_code == 200
        user_list = res.json["data"]
        assert len(user_list) == 2

        # cleanup
        self.cleanup_entires()

    def test_payment_method_list(self):
        # create users and bank accounts and credit card
        self.create_payer_payee_user()
        self.create_bank_account(10000)
        self.create_credit_card(2000)
        self.create_debit_card()

        url = f"{self.base_url}/get_all_payment_methods/{self.payer_id}"
        res = self.app_client.get(url)
        assert res.status_code == 200 
        payment_list = res.json["data"]
        assert len(payment_list) == 3

        # cleanup
        self.cleanup_entires()
    
    def test_payment_method_list_failure(self):
        # create users and bank accounts and credit card
        self.create_payer_payee_user()

        url = f"{self.base_url}/get_all_payment_methods/0"
        res = self.app_client.get(url)
        assert res.status_code == 404 
        assert res.json == {"message": "User does not exists"}

        # cleanup
        self.cleanup_entires()

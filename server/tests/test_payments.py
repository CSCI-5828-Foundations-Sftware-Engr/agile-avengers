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
        self.payer_id = None
        self.payee_id = None
        self.transaction_id  = None
        self.base_url = "/v1/payment"

    def teardown_class(self):
        self.cleanup_entires(self)
        self.session.rollback()
        self.session.close()
    
    def create_payer_payee_user(self):
        payer = UserInfo(
            user_name = "preetham",
            first_name = "Preetham",
            last_name = "Maiya",
            mobile_number = "1234566789",
            email_id = "prma6536@colorado.edu",
            is_merchant = False,
            created_on = datetime.now(),
            created_by = "preetham",
            updated_on = datetime.now(),
            updated_by = "preetham",
        )

        payee = UserInfo(
            # user_id = 2,
            user_name = "ashutosh",
            first_name = "Ashutosh",
            last_name = "Gandhi",
            mobile_number = "1234566289",
            email_id = "asga5889@colorado.edu",
            is_merchant = False,
            created_on = datetime.now(),
            created_by = "ashutosh",
            updated_on = datetime.now(),
            updated_by = "ashutosh",
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
    
    def create_req_transaction(self):
        transaction = Transaction(
            payer_id = self.payer_id,
            payee_id = self.payee_id,
            transaction_amount = 100,
            is_completed = False,
            created_by = self.payee_id,
            created_on = datetime.now()
        )
        self.session.add(transaction)
        self.session.commit()

        self.transaction_id = transaction.transaction_id
    
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

        self.cleanup_entires()
    
    def test_payment_method_list_failure(self):
        # create users
        self.create_payer_payee_user()

        url = f"{self.base_url}/get_all_payment_methods/0"
        res = self.app_client.get(url)
        assert res.status_code == 404 
        assert res.json == {"message": "User does not exists"}

        self.cleanup_entires()

    def test_invalid_payer(self):
        url = f"{self.base_url}/send"
        # create users
        self.create_payer_payee_user()
        
        req = {
            "payer_id": 0,
            "payee_id": self.payee_id,
            "transaction_amount": 100,
            "transaction_method": "credit",
            "transaction_method_id": "1234567891234568"
        }

        res = self.app_client.post(url, json=req)
        assert res.status_code == 400
        assert res.json == {"message": "Payer does not exists"}
        
        self.cleanup_entires()
    
    def test_invalid_payee(self):
        url = f"{self.base_url}/send"
        # create users
        self.create_payer_payee_user()
        
        req = {
            "payer_id": self.payer_id,
            "payee_id": 0,
            "transaction_amount": 100,
            "transaction_method": "credit",
            "transaction_method_id": "1234567891234568"
        }

        res = self.app_client.post(url, json=req)
        assert res.status_code == 400
        assert res.json == {"message": "Payee does not exists"}
        
        self.cleanup_entires()
    
    def test_insufficient_bank_balance(self):
        url = f"{self.base_url}/send"

        # create users and bank accounts
        self.create_payer_payee_user()
        self.create_bank_account(1000)

        req = {
            "payer_id": self.payer_id,
            "payee_id": self.payee_id,
            "transaction_amount": 5000,
            "transaction_method": "bank",
            "transaction_method_id": "123456789123423567"
        }

        res = self.app_client.post(url, json=req)
        assert res.status_code == 400
        assert res.json == {"message": "Insufficient funds, transaction cannot take place"}

        self.cleanup_entires()
    
    def test_insufficient_bank_balance_debit(self):
        url = f"{self.base_url}/send"

        # create users and bank accounts and debit card
        self.create_payer_payee_user()
        self.create_bank_account(1000)
        self.create_debit_card()

        req = {
            "payer_id": self.payer_id,
            "payee_id": self.payee_id,
            "transaction_amount": 5000,
            "transaction_method": "debit",
            "transaction_method_id": "1234567891234567"
        }
        
        res = self.app_client.post(url, json=req)
        assert res.status_code == 400
        assert res.json == {"message": "Insufficient funds, transaction cannot take place"}

        self.cleanup_entires()
    
    def test_insufficient_credit_limit(self):
        url = f"{self.base_url}/send"

        # create users and bank accounts and credit card
        self.create_payer_payee_user()
        self.create_bank_account(10000)
        self.create_credit_card(2000)

        req = {
            "payer_id": self.payer_id,
            "payee_id": self.payee_id,
            "transaction_amount": 3000,
            "transaction_method": "credit",
            "transaction_method_id": "1234567891234568"
        }

        res = self.app_client.post(url, json=req)
        assert res.status_code == 400
        assert res.json == {"message": "Insufficient funds, transaction cannot take place"}

        self.cleanup_entires()
    
    def test_invalid_method_id(self):
        url = f"{self.base_url}/send"

        # create users and bank accounts and credit card
        self.create_payer_payee_user()
        self.create_bank_account(10000)
        self.create_credit_card(2000)
        self.create_debit_card()

        # invalid credit card
        req = {
            "payer_id": self.payer_id,
            "payee_id": self.payee_id,
            "transaction_amount": 3000,
            "transaction_method": "credit",
            "transaction_method_id": "12345678912"
        }
        res = self.app_client.post(url, json=req)
        assert res.status_code == 400
        assert res.json == {"message": "Transaction method is incorrect. No corresponding credit card account found."}

        # invalid debit card 
        req = {
            "payer_id": self.payer_id,
            "payee_id": self.payee_id,
            "transaction_amount": 5000,
            "transaction_method": "debit",
            "transaction_method_id": "12345678912"
        }
        res = self.app_client.post(url, json=req)
        assert res.status_code == 400
        assert res.json == {"message": "Transaction method is incorrect. No corresponding debit card account found."}

        # invalid bank account
        req = {
            "payer_id": self.payer_id,
            "payee_id": self.payee_id,
            "transaction_amount": 5000,
            "transaction_method": "bank",
            "transaction_method_id": "123456789123"
        }

        res = self.app_client.post(url, json=req)
        assert res.status_code == 400
        assert res.json == {"message": "Transaction method is incorrect. No corresponding bank account found."}
        
        self.cleanup_entires()
    
    def test_request_payment(self):
        url = f"{self.base_url}/request"

        # create users and bank accounts
        self.create_payer_payee_user()
        self.create_bank_account(10000)
        
        req = {
            "requestor_id": self.payee_id,
            "sender_id": self.payer_id,
            "transaction_amount": 100
        }
        res = self.app_client.post(url, json=req)
        assert res.status_code == 201
        transaction_id = res.json["id"]
        transaction = self.session.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
        assert transaction != None # check if transaction is created
        assert transaction.is_completed == False

        self.session.query(Transaction).filter(Transaction.transaction_id == transaction_id).delete()
        self.cleanup_entires()
    
    def test_pending_requests(self):
        # create users and bank accounts
        self.create_payer_payee_user()
        self.create_bank_account(10000)
        
        url = f"{self.base_url}/pending_requests/{self.payer_id}"

        transaction = Transaction(
            payer_id = self.payer_id,
            payee_id = self.payee_id,
            transaction_amount = 100,
            is_completed = False,
            created_by = self.payee_id,
            created_on = datetime.now()
        )
        self.session.add(transaction)
        self.session.commit()

        transaction_id = transaction.transaction_id
        req = self.app_client.get(url)
        assert req.status_code == 200
        request_list = req.json["data"]
        assert len(request_list) == 1
        assert request_list[0]["requestor_id"] == self.payee_id
        assert request_list[0]["transaction_id"] == transaction_id
        assert request_list[0]["transaction_amount"] == 100
        assert request_list[0]["requestor_name"] == "Ashutosh Gandhi"

        self.session.query(Transaction).filter(Transaction.transaction_id == transaction_id).delete()
        self.cleanup_entires()

    
    def test_transaction_completion(self):
        # create users and bank accounts
        self.create_payer_payee_user()
        self.create_bank_account(10000)
        self.create_credit_card(2000)
        self.create_debit_card()
        self.create_req_transaction()

        url = f"{self.base_url}/send/{self.transaction_id}"
        
        # test transfer using bank account
        req = {
            "payer_id": self.payer_id,
            "payee_id": self.payee_id,
            "transaction_amount": 100,
            "transaction_method": "bank",
            "transaction_method_id": "123456789123423567"
        }

        res = self.app_client.post(url, json=req)
        self.assert_balance(res, "bank") # assert balance updation
        transaction = self.session.query(Transaction).filter(Transaction.transaction_id == self.transaction_id).first()
        assert transaction.is_completed == True
        assert int(transaction.updated_by) == self.payer_id

        self.session.query(Transaction).filter(Transaction.transaction_id == self.transaction_id).delete()
        self.cleanup_entires()
    
    def test_transaction_completion_credit(self):
        # create users and bank accounts and credit card
        self.create_payer_payee_user()
        self.create_bank_account(10000)
        self.create_credit_card(2000)
        self.create_req_transaction()

        url = f"{self.base_url}/send/{self.transaction_id}"
        req = {
            "payer_id": self.payer_id,
            "payee_id": self.payee_id,
            "transaction_amount": 100,
            "transaction_method": "credit",
            "transaction_method_id": "1234567891234568"
        }
        res = self.app_client.post(url, json=req)
        self.assert_balance(res, "credit")
        transaction = self.session.query(Transaction).filter(Transaction.transaction_id == self.transaction_id).first()
        assert transaction.is_completed == True
        assert int(transaction.updated_by) == self.payer_id

        self.session.query(Transaction).filter(Transaction.transaction_id == self.transaction_id).delete()
        self.cleanup_entires()
    

    def test_transaction_completion_debit(self):
        # create users and bank accounts and debit card
        self.create_payer_payee_user()
        self.create_bank_account(10000)
        self.create_debit_card()
        self.create_req_transaction()
        
        url = f"{self.base_url}/send/{self.transaction_id}"
        req = {
            "payer_id": self.payer_id,
            "payee_id": self.payee_id,
            "transaction_amount": 100,
            "transaction_method": "debit",
            "transaction_method_id": "1234567891234567"
        }

        res = self.app_client.post(url, json=req)
        self.assert_balance(res, "debit") # assert balance updation
        transaction = self.session.query(Transaction).filter(Transaction.transaction_id == self.transaction_id).first()
        assert transaction.is_completed == True
        assert int(transaction.updated_by) == self.payer_id

        self.session.query(Transaction).filter(Transaction.transaction_id == self.transaction_id).delete()
        self.cleanup_entires()

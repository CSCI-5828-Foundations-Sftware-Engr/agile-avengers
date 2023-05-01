from faker import Faker
import faker.providers as providers
import random as r
import src.config as config
import traceback

# initialize object and add providers
fake = Faker()
fake.add_provider(providers.profile)
fake.add_provider(providers.person)
fake.add_provider(providers.credit_card)
fake.add_provider(providers.bank)
fake.add_provider(providers.address)

def generate_phone_number():
    ph_no = []
  
    # the first number should be in the range of 6 to 9
    ph_no.append(r.randint(6, 9))
    
    # the for loop is used to append the other 9 numbers.
    # the other 9 numbers can be in the range of 0 to 9.
    for _ in range(1, 10):
        ph_no.append(r.randint(0, 9))

    return ''.join(map(str,ph_no))

def generate_balance():
    return fake.random_int(min=config.min_balance, max=config.max_balance, step=100)

def generate_user_info():
    profile = fake.simple_profile()
    user_info = {
        "username": profile["username"],
        "password": fake.password(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email_id": profile["mail"],
        "mobile_number": generate_phone_number(),
        "is_merchant": False
    }
    return user_info

def generate_bank_info():
   bank_info = {
       "account_number": fake.bban(),
       "account_holders_name": f"{fake.first_name()} {fake.first_name()}",
       "bank_name": fake.credit_card_provider(),
       "routing_number": fake.aba()
    }
   return bank_info

def generate_credit_card():
    credit_info = {
        "billing_address": fake.street_address(),
        "postal_code": fake.postcode(),
        "state": fake.country_code(),
        "city": fake.city(),
        "card_number": fake.credit_card_number()[:16],
        "card_network": fake.credit_card_provider(),
        "cvv": fake.credit_card_security_code()
    }
    return credit_info
    

def generate_fake_data():
    usernames = []
    users = {}
    transactions = []
    methods = ["bank", "credit"]

    # generate users
    for _ in range(5):
        user_info = generate_user_info()
        usernames.append(user_info["username"])
        users[user_info["username"]] = {
            "user_info": user_info,
            "bank_info": generate_bank_info(),
            "credit_info": generate_credit_card()
        }

    # generate transactions between them
    for _ in range(20):
        user1, user2 = r.sample(usernames, 2)
        method = r.choice(methods)
        try:
            if method == "bank":
                transactions.append(
                    {
                        "payer_id": user1,
                        "payee_id": user2,
                        "transaction_amount": fake.random_int(min=10, max=500, step=5),
                        "transaction_method": "bank",
                        "transaction_method_id": users[user1]["bank_info"]["account_number"]
                    }
                )
            elif method == "credit":
                transactions.append(
                    {
                        "payer_id": user1,
                        "payee_id": user2,
                        "transaction_amount": fake.random_int(min=10, max=500, step=5),
                        "transaction_method": "credit",
                        "transaction_method_id": users[user1]["credit_info"]["card_number"]
                    }
                )
        
        except Exception as ex:
            traceback.print_exc()
            print("Skip this entry")
    
    return {
        "users": users, # type(users) = dict
        "transactions": transactions # type(transactions) = list
    }
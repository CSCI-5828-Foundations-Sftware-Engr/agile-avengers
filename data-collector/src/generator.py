from faker import Faker
import faker.providers as providers
import random as r
import src.config as config

# initialize object and add providers
fake = Faker()
fake.add_provider(providers.profile)
fake.add_provider(providers.person)
fake.add_provider(providers.credit_card)
fake.add_provider(providers.bank)

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
    profile = fake.simple_profile()
    address = profile["address"]
    credit_info = {
        "billing_address": address.split("\n")[0],
        "postal_code": address.split("\n")[1].split(',')[1].strip().split()[1],
        "state": address.split("\n")[1].split(',')[1].strip().split()[0],
        "city": address.split("\n")[1].split(',')[0],
        "card_number": fake.credit_card_number(),
        "card_network": fake.credit_card_provider(),
        "cvv": fake.credit_card_security_code()
    }
    return credit_info
    
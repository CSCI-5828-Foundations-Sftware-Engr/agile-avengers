import time
import pytest
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class AddPaymentFormValidation(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def tearDown(self):
        self.driver.quit()

    def test_add_payment_credit_form_validation(self):
        # Load the login form
        self.driver.get("http://localhost:8081/login")

        # Let the timer sleep for 2 seconds until the page loads
        time.sleep(2)

        # Fill in the username field with valid input
        username_input = self.driver.find_element(By.ID, "username")
        username_input.send_keys("testuser11")

        # Fill in the password field with invalid input
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys("invalidpassword")

        # Submit the form
        submit_button = self.driver.find_element(By.XPATH, "//button[text()='Login']")
        submit_button.click()

        # Wait for 2 seconds for the page to load
        time.sleep(2)

        # Verify that the user is redirected to the payment page with the correct query parameter
        expected_url = "http://localhost:8081/payment"
        self.assertEqual(self.driver.current_url, expected_url)

        # Click on the 'Add Payment' link
        add_payment_link = self.driver.find_element(By.XPATH,"//a[@href='/add_payment_method']")
        add_payment_link.click()

        # Wait for 2 seconds for the page to load
        time.sleep(2)

        # Verify that the user is redirected to the add payment page with the correct query parameter
        expected_url = "http://localhost:8081/add_payment_method"
        self.assertEqual(self.driver.current_url, expected_url)

        # select "Credit Card" option from dropdown
        payment_method_dropdown = Select(self.driver.find_element(By.ID, "paymentMethodType"))
        payment_method_dropdown.select_by_value("creditCard")

        # Wait for 2 seconds for the fields to get populated
        time.sleep(2)

        # fill in Credit Card details
        card_name_input = self.driver.find_element(By.ID,"cardName")
        card_name_input.send_keys("Test09")
        card_type_dropdown = Select(self.driver.find_element(By.ID, "cardType"))
        card_type_dropdown.select_by_value("visa")
        card_number_input = self.driver.find_element(By.ID,"cardNumber")
        card_number_input.send_keys("1234567890123456")
        expiry_month_input = self.driver.find_element(By.ID,"expirationDate")
        expiry_month_input.send_keys("09/2037")
        cvv_input = self.driver.find_element(By.ID,"securityCode")
        cvv_input.send_keys("123")
        first_name_on_card_input = self.driver.find_element(By.ID,"billingFirstName")
        first_name_on_card_input.send_keys("John")
        last_name_on_card_input = self.driver.find_element(By.ID,"billingLastName")
        last_name_on_card_input.send_keys("Smith")
        billing_add_input = self.driver.find_element(By.ID,"billingAddress")
        billing_add_input.send_keys("ABC 123, LAX")
        billing_city_input = self.driver.find_element(By.ID,"billingCity")
        billing_city_input.send_keys("ABCDE")
        billing_state_input = self.driver.find_element(By.ID,"billingState")
        billing_state_input.send_keys("PA")
        billing_postal_input = self.driver.find_element(By.ID,"billingPostalCode")
        billing_postal_input.send_keys("90876")

        # submit the form
        submit_button = self.driver.find_element(By.CSS_SELECTOR,".btn-primary")
        submit_button.click()

        # wait for the success message
        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, ".toast_col2"))
        )
        
        # assert that the success message contains the expected text
        self.assertIn("Credit Card has been successfully added!", success_message.text)        

    def test_add_payment_bank_acc_form_validation(self):
        # Load the login form
        self.driver.get("http://localhost:8081/login")

        # Let the timer sleep for 2 seconds until the page loads
        time.sleep(2)

        # Fill in the username field with valid input
        username_input = self.driver.find_element(By.ID, "username")
        username_input.send_keys("testuser11")

        # Fill in the password field with invalid input
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys("invalidpassword")

        # Submit the form
        submit_button = self.driver.find_element(By.XPATH, "//button[text()='Login']")
        submit_button.click()

        # Wait for 2 seconds for the page to load
        time.sleep(2)

        # Verify that the user is redirected to the payment page with the correct query parameter
        expected_url = "http://localhost:8081/payment"
        self.assertEqual(self.driver.current_url, expected_url)

        # Click on the 'Add Payment' link
        add_payment_link = self.driver.find_element(By.XPATH,"//a[@href='/add_payment_method']")
        add_payment_link.click()

        # Wait for 2 seconds for the page to load
        time.sleep(2)

        # Verify that the user is redirected to the add payment page with the correct query parameter
        expected_url = "http://localhost:8081/add_payment_method"
        self.assertEqual(self.driver.current_url, expected_url)

        # select "Credit Card" option from dropdown
        payment_method_dropdown = Select(self.driver.find_element(By.ID, "paymentMethodType"))
        payment_method_dropdown.select_by_value("bankAccount")

        # Wait for 2 seconds for the fields to get populated
        time.sleep(2)

        # fill in Bank account details
        account_type_dropdown = Select(self.driver.find_element(By.ID, "accountType"))
        account_type_dropdown.select_by_value("checkingAccount")
        account_name_input = self.driver.find_element(By.ID,"accountHolderName")
        account_name_input.send_keys("Test09")
        account_number_input = self.driver.find_element(By.ID,"accountNumber")
        account_number_input.send_keys("123456781")
        routing_number_input = self.driver.find_element(By.ID,"routingNumber")
        routing_number_input.send_keys("1234567")
        bank_name_input = self.driver.find_element(By.ID,"bankName")
        bank_name_input.send_keys("Chase")

        # submit the form
        submit_button = self.driver.find_element(By.CSS_SELECTOR,".btn-primary")
        submit_button.click()

        # wait for the success message
        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, ".toast_col2"))
        )
        
        # assert that the success message contains the expected text
        self.assertIn("Bank account has been successfully added", success_message.text)        

    @pytest.mark.skip(reason="This test is not ready yet")
    def test_add_payment_debit_form_validation(self):
        # Load the login form
        self.driver.get("http://localhost:8081/login")

        # Let the timer sleep for 2 seconds until the page loads
        time.sleep(2)

        # Fill in the username field with valid input
        username_input = self.driver.find_element(By.ID, "username")
        username_input.send_keys("testuser11")

        # Fill in the password field with invalid input
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys("invalidpassword")

        # Submit the form
        submit_button = self.driver.find_element(By.XPATH, "//button[text()='Login']")
        submit_button.click()

        # Wait for 2 seconds for the page to load
        time.sleep(2)

        # Verify that the user is redirected to the payment page with the correct query parameter
        expected_url = "http://localhost:8081/payment"
        self.assertEqual(self.driver.current_url, expected_url)

        # Click on the 'Add Payment' link
        add_payment_link = self.driver.find_element(By.XPATH,"//a[@href='/add_payment_method']")
        add_payment_link.click()

        # Wait for 2 seconds for the page to load
        time.sleep(2)

        # Verify that the user is redirected to the add payment page with the correct query parameter
        expected_url = "http://localhost:8081/add_payment_method"
        self.assertEqual(self.driver.current_url, expected_url)

        # select "Credit Card" option from dropdown
        payment_method_dropdown = Select(self.driver.find_element(By.ID, "paymentMethodType"))
        payment_method_dropdown.select_by_value("debitCard")

        # Wait for 2 seconds for the fields to get populated
        time.sleep(2)

        # fill in Credit Card details
        card_name_input = self.driver.find_element(By.ID,"cardName")
        card_name_input.send_keys("Test09")
        card_network_dropdown = Select(self.driver.find_element(By.ID, "cardType"))
        card_network_dropdown.select_by_value("visa")
        card_number_input = self.driver.find_element(By.ID,"cardNumber")
        card_number_input.send_keys("1234567890123456")
        expiry_month_input = self.driver.find_element(By.ID,"expirationDate")
        expiry_month_input.send_keys("09/2037")
        cvv_input = self.driver.find_element(By.ID,"securityCode")
        cvv_input.send_keys("123")
        first_name_on_card_input = self.driver.find_element(By.ID,"billingFirstName")
        first_name_on_card_input.send_keys("John")
        last_name_on_card_input = self.driver.find_element(By.ID,"billingLastName")
        last_name_on_card_input.send_keys("Smith")
        billing_add_input = self.driver.find_element(By.ID,"billingAddress")
        billing_add_input.send_keys("ABC 123, LAX")
        billing_city_input = self.driver.find_element(By.ID,"billingCity")
        billing_city_input.send_keys("ABCDE")
        billing_state_input = self.driver.find_element(By.ID,"billingState")
        billing_state_input.send_keys("PA")
        billing_postal_input = self.driver.find_element(By.ID,"billingPostalCode")
        billing_postal_input.send_keys("90876")

        # submit the form
        submit_button = self.driver.find_element(By.CSS_SELECTOR,".btn-primary")
        submit_button.click()

        # wait for the success message
        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, ".toast_col2"))
        )
        
        # assert that the success message contains the expected text
        self.assertIn("Credit Card has been successfully added!", success_message.text)        


if __name__ == "__main__":
    unittest.main()
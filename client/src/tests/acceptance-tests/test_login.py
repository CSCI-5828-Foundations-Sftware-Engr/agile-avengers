import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class LoginFormValidation(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def tearDown(self):
        self.driver.quit()

    def test_login_form_validation(self):
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

        # Verify that various tabs after logging in are shown
        payment_link = self.driver.find_element(By.XPATH,"//a[@href='/payment']")
        self.assertEqual(payment_link.text, "Send or Request Payment")
        add_payment_link = self.driver.find_element(By.XPATH,"//a[@href='/add_payment_method']")
        self.assertEqual(add_payment_link.text, "Add Payment Methods")
        transaction_link = self.driver.find_element(By.XPATH,"//a[@href='/transaction']")
        self.assertEqual(transaction_link.text, "Transactions")

        # Verify that the user is redirected to the payment page with the correct query parameter
        expected_url = "http://localhost:8081/payment"
        self.assertEqual(self.driver.current_url, expected_url)

        # Logout the user
        logout_link = self.driver.find_element(By.CLASS_NAME,"ml-auto")
        logout_link.click()

        # Wait for 2 seconds for the page to load
        time.sleep(2)

        # Verify if the login page is back
        expected_url = "http://localhost:8081/login"
        self.assertEqual(self.driver.current_url, expected_url)

if __name__ == "__main__":
    unittest.main()
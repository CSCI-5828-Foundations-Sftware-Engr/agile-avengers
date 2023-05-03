import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class PendingPaymentFormValidation(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def tearDown(self):
        self.driver.quit()

    def test_pending_payment_form_validation(self):
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

        # Click on the 'Send or Request Payment' link
        add_payment_link = self.driver.find_element(By.XPATH,"//a[@href='/payment']")
        add_payment_link.click()

        # Wait for 2 seconds for the page to load
        time.sleep(2)

        # Verify that the user is redirected to the payment page with the correct query parameter
        expected_url = "http://localhost:8081/payment"
        self.assertEqual(self.driver.current_url, expected_url)

        # select "Pending Payment" option from dropdown
        payment_method_dropdown = Select(self.driver.find_element(By.ID, "paymentMethodType"))
        payment_method_dropdown.select_by_value("pendingPaymentRequests")

        # Wait for 2 seconds for the fields to get populated
        time.sleep(2)

        # fill in details
        user_to_pay_input = self.driver.find_element(By.ID,"payee")
        user_to_pay_input.select_by_index(1)
        amount_input = self.driver.find_element(By.ID,"amountToSend")
        amount_input.send_keys(10)

        # submit the form
        submit_button = self.driver.find_element(By.CSS_SELECTOR,".btn-primary")
        submit_button.click()

        # wait for the success message
        # success_message = WebDriverWait(self.driver, 10).until(
        #     EC.visibility_of_element_located((By.CLASS_NAME, ".toast_col2"))
        # )
        
        # assert that the success message contains the expected text
        # self.assertIn("Credit Card has been successfully added!", success_message.text)        

if __name__ == "__main__":
    unittest.main()
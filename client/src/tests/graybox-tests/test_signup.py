import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class SignupFormValidation(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def tearDown(self):
        self.driver.quit()

    def test_signup_form_validation_user1(self):
        # Load the Signup form
        self.driver.get("http://localhost:8081/signup")

        # Let the timer sleep for 2 seconds until the page loads
        time.sleep(2)

        # Fill in the username field with valid input
        username_input = self.driver.find_element(By.ID, "username")
        username_input.send_keys("testuser11")

        # Fill in the password field
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys("invalidpassword")

        # Fill in the confirm password field with different invalid input
        confirm_password_input = self.driver.find_element(By.ID, "confirmPassword")
        confirm_password_input.send_keys("10differentpassword")

        # Submit the form
        submit_button = self.driver.find_element(By.XPATH, "//button[text()='Sign Up']")
        submit_button.click()

        # Verify that an error message is displayed
        error_message = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert"))
        )
        self.assertEqual(error_message.text, "Passwords do not match")

        # Fill in the confirm password field with valid input
        confirm_password_input.clear()
        confirm_password_input.send_keys("invalidpassword")

        # Submit the form again
        submit_button.click()

        # Wait for 2 seconds for the page to load
        time.sleep(2)

        # This will load the next webpage to enter further user info details
        # Fill in the firstname field with valid input
        firstname_input = self.driver.find_element(By.ID, "firstName")
        firstname_input.send_keys("testuser123")

        # Fill in the lastname field with valid input
        lastname_input = self.driver.find_element(By.ID, "lastName")
        lastname_input.send_keys("321usertest")

        # Fill in an invalid mobile number
        mobnum_input = self.driver.find_element(By.ID, "mobileNumber")
        mobnum_input.send_keys("99887766")

        # Fill in a valid email id
        email_input = self.driver.find_element(By.ID, "emailId")
        email_input.send_keys("abc@gmail.com")

        # Submit the form
        submit_button = self.driver.find_element(By.XPATH, "//button[text()='Create Account']")
        submit_button.click()

        # Error will appear saying mobile number is invalid
        error_message = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert"))
        )
        self.assertEqual(error_message.text, "Invalid mobile number")

        # Fill in the mobile number field with valid input
        mobnum_input.clear()
        mobnum_input.send_keys("9988776655")

        # Submit the form again
        submit_button.click()

        # Wait for 2 seconds for the new page to be redirected
        time.sleep(2)

        # Verify that a success message is displayed
        success_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )
        self.assertEqual(success_message.text, "Account created successfully")

        # Verify that the user is redirected to the createuser page with the correct query parameter
        expected_url = "http://localhost:8081/login?success=true"
        self.assertEqual(self.driver.current_url, expected_url)

    def test_signup_form_validation_user2(self):
        # Another user is created but not validated 
        # This is done so that the send/recieve payment can be shown
        self.driver.get("http://localhost:8081/signup")
        time.sleep(2)

        username_input = self.driver.find_element(By.ID, "username")
        username_input.send_keys("testuser22")

        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys("invalidpassword")

        confirm_password_input = self.driver.find_element(By.ID, "confirmPassword")
        confirm_password_input.send_keys("invalidpassword")

        submit_button = self.driver.find_element(By.XPATH, "//button[text()='Sign Up']")
        submit_button.click()

        time.sleep(2)

        firstname_input = self.driver.find_element(By.ID, "firstName")
        firstname_input.send_keys("testuser1234")

        lastname_input = self.driver.find_element(By.ID, "lastName")
        lastname_input.send_keys("4321usertest")

        mobnum_input = self.driver.find_element(By.ID, "mobileNumber")
        mobnum_input.send_keys("9988776666")

        email_input = self.driver.find_element(By.ID, "emailId")
        email_input.send_keys("abc@gmail.com")

        submit_button = self.driver.find_element(By.XPATH, "//button[text()='Create Account']")
        submit_button.click()

        time.sleep(2)

        success_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )
        self.assertEqual(success_message.text, "Account created successfully")

        expected_url = "http://localhost:8081/login?success=true"
        self.assertEqual(self.driver.current_url, expected_url)


if __name__ == "__main__":
    unittest.main()
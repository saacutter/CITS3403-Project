import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class SeleniumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)
        cls.base_url = "http://localhost:5000"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_signup_create_tournament_and_check_homepage(self):
        driver = self.driver
        driver.get(self.base_url + "/signup")

        # Fill out the signup form with a unique details
        username = f"Malcom123{int(time.time())}"
        email = f"{username}@example.com"
        password = "ThisISAstrongPassword!"

        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password_confirm").send_keys(password)
        driver.find_element(By.NAME, "submit").click()

        # Wait for redirect to homepage after signup
        time.sleep(1)
        driver.get(self.base_url + "/")

        # Serelium checks if there is a button called Add Tournament, then clicks it
        add_btn = driver.find_element(By.LINK_TEXT, "Add Tournament")
        add_btn.click()

        # Serelium fills out the details of the add tournament page then clicks submit
        driver.find_element(By.NAME, "name").send_keys("Crash Bandicoot Racing Championship")
        driver.find_element(By.NAME, "game").send_keys("Crash Bandicoot")
        driver.find_element(By.NAME, "date").send_keys("2025-05-20")
        driver.find_element(By.NAME, "details").send_keys("This is a serelim test, lets see if this works.")
        driver.find_element(By.NAME, "points").send_keys("42")
        driver.find_element(By.NAME, "result").send_keys("win")
        driver.find_element(By.NAME, "submit").click()

        # Serelium then goes back to the home page
        time.sleep(1)
        driver.get(self.base_url + "/")

        # It then checks if the tournament is on the homepage which would indicate that it has been successfully uploaded and retrieved from the database
        self.assertIn("Selenium Test Tournament", driver.page_source)

if __name__ == "__main__":
    unittest.main()
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)
        cls.base_url = "http://127.0.0.1:5000"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_signup_create_tournament_and_check_homepage(self):
        driver = self.driver
        driver.get(self.base_url + "/")

        # Click signup button
        login_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "signup-btn"))
        )
        login_btn.click()

        time.sleep(1)

        # Wait for signup form fields to be visible and interactable
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username"))
        )
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        password_confirm_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "password_confirm"))
        )

        # Toggle off "Make my profile private" if it is checked
        private_checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "private"))
        )
        if private_checkbox.is_selected():
            label = driver.find_element(By.CSS_SELECTOR, "label[for='private']")
            label.click()

        username_field.send_keys("Eddy123")
        email_field.send_keys("Eddy123@example.com")
        password_field.send_keys("ThisISAstrongPassword!")
        password_confirm_field.send_keys("ThisISAstrongPassword!")

        time.sleep(3)

        # Submit the form
        submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "submit"))
        )
        submit_btn.click()

        time.sleep(3)

        # Wait for homepage to load by checking for the "Create New Tournament" button
        add_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Create New Tournament"))
        )
        add_btn.click()

        time.sleep(1)

        # Wait for tournament form fields to be visible
        name_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "name"))
        )
        game_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "game"))
        )
        date_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "date"))
        )
        details_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "details"))
        )
        points_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "points"))
        )
        result_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "result"))
        )

        name_field.send_keys("Crash Bandicoot Championship")
        game_field.send_keys("Crash Bandicoot")
        date_field.send_keys("2025-05-20")
        details_field.send_keys("This is a serelim test, lets see if this works.")
        points_field.send_keys("42")
        result_field.send_keys("win")

        time.sleep(3)

        driver.find_element(By.NAME, "submit").click()

        # Wait for homepage to load and check for tournament name in any element
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Crash Bandicoot Championship')]")
        self.assertTrue(len(elements) > 0, "Tournament not found on homepage")

        time.sleep(7)

if __name__ == "__main__":
    unittest.main()
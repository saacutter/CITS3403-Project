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

    def test_signup(self):
        driver = self.driver
        driver.get(self.base_url + "/signout")
        signup_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "signup-btn"))
        )
        signup_btn.click()
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username"))
        )
        email_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.ID, "password")
        password_confirm_field = driver.find_element(By.ID, "password_confirm")
        # Toggle off private if checked
        private_checkbox = driver.find_element(By.ID, "private")
        if private_checkbox.is_selected():
            label = driver.find_element(By.CSS_SELECTOR, "label[for='private']")
            label.click()
        username_field.send_keys("TestUser4")
        email_field.send_keys("testuser4@example.com")
        password_field.send_keys("TestPassword123!")
        password_confirm_field.send_keys("TestPassword123!")
        driver.find_element(By.NAME, "submit").click()
        # Check for successful registration (e.g., homepage loaded)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Create New Tournament"))
        )

    def test_signup_create_tournament_and_check_homepage(self):
        driver = self.driver
        driver.get(self.base_url + "/signout")

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

        username_field.send_keys("Frank123")
        email_field.send_keys("Frank123@example.com")
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

    def test_edit_tournament(self):
        driver = self.driver
        driver.get(self.base_url + "/signout")

        # --- Sign up a new user ---
        signup_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "signup-btn"))
        )
        signup_btn.click()
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username"))
        )
        email_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.ID, "password")
        password_confirm_field = driver.find_element(By.ID, "password_confirm")
        private_checkbox = driver.find_element(By.ID, "private")
        if private_checkbox.is_selected():
            label = driver.find_element(By.CSS_SELECTOR, "label[for='private']")
            label.click()
        username_field.send_keys("EditUser9")
        email_field.send_keys("edituser9@example.com")
        password_field.send_keys("EditPassword123!")
        password_confirm_field.send_keys("EditPassword123!")
        driver.find_element(By.NAME, "submit").click()

        # --- Create a tournament ---
        add_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Create New Tournament"))
        )
        add_btn.click()
        name_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "name"))
        )
        game_field = driver.find_element(By.NAME, "game")
        date_field = driver.find_element(By.NAME, "date")
        details_field = driver.find_element(By.NAME, "details")
        points_field = driver.find_element(By.NAME, "points")
        result_field = driver.find_element(By.NAME, "result")
        name_field.send_keys("Crossy Road Battle")
        game_field.send_keys("Crossy Road")
        date_field.send_keys("2025-06-02")
        details_field.send_keys("Original tournament details.")
        points_field.send_keys("5")
        result_field.send_keys("win")
        driver.find_element(By.NAME, "submit").click()

        # --- Go to tournaments page and edit the tournament ---
        driver.get(self.base_url + "/user/EditUser6")
        # Find the edit button for the tournament (adjust selector as needed)
        edit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Edit Tournament')]"))
        )
        edit_btn.click()
        # Edit details
        details_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "details"))
        )
        details_field.clear()
        details_field.send_keys("Tournament edited by Selenium test.")
        driver.find_element(By.NAME, "submit").click()
        # Check for updated details
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Tournament edited by Selenium test.')]")
        visible_elements = [el for el in elements if el.is_displayed()]
        self.assertTrue(len(visible_elements) > 0, "Edited tournament details not found on the visible page")

    def test_edit_profile(self):
        driver = self.driver
        driver.get(self.base_url + "/signout")
        time.sleep(1)

        # --- Sign up a new user ---
        signup_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "signup-btn"))
        )
        signup_btn.click()
        time.sleep(1)
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username"))
        )
        email_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.ID, "password")
        password_confirm_field = driver.find_element(By.ID, "password_confirm")
        private_checkbox = driver.find_element(By.ID, "private")
        if private_checkbox.is_selected():
            label = driver.find_element(By.CSS_SELECTOR, "label[for='private']")
            label.click()
        username_field.send_keys("ProfileEditUser6")
        email_field.send_keys("profileedituser6@example.com")
        password_field.send_keys("ProfileEditPassword123!")
        password_confirm_field.send_keys("ProfileEditPassword123!")
        time.sleep(1)
        driver.find_element(By.NAME, "submit").click()
        time.sleep(2)

        # --- Go to user profile page ---
        driver.get(self.base_url + "/user/ProfileEditUser6")
        time.sleep(1)

        # --- Click edit profile button (adjust selector as needed) ---
        edit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Edit Profile"))
        )
        edit_btn.click()
        time.sleep(1)

        # --- Edit profile info (e.g., bio) ---
        new_username = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        )
        new_username.clear()
        new_username.send_keys("Gus")
        time.sleep(1)
        driver.find_element(By.NAME, "submit").click()
        time.sleep(2)

        # --- Check for updated username ---
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Gus')]")
        self.assertTrue(len(elements) > 0, "Updated username not found on profile")

    def test_private_user(self):
        driver = self.driver
        driver.get(self.base_url + "/signout")

        # --- Sign up a new user with private profile (leave private checked) ---
        signup_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "signup-btn"))
        )
        signup_btn.click()
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username"))
        )
        email_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.ID, "password")
        password_confirm_field = driver.find_element(By.ID, "password_confirm")
        # Do NOT toggle off private checkbox (leave as default checked)
        username_field.send_keys("PrivateUser3")
        email_field.send_keys("privateuser3@example.com")
        password_field.send_keys("PrivatePassword123!")
        password_confirm_field.send_keys("PrivatePassword123!")
        driver.find_element(By.NAME, "submit").click()

        # --- Go to user profile page ---
        driver.get(self.base_url + "/user/PrivateUser3")

        # --- Click edit profile button ---
        edit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Edit Profile"))
        )
        edit_btn.click()

        # --- Check if private toggle is checked ---
        private_checkbox = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "private"))
        )
        self.assertTrue(private_checkbox.is_selected(), "Private profile toggle should be checked in edit profile")

if __name__ == "__main__":
    unittest.main()
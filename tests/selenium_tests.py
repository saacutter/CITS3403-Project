import unittest
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from app import create_application, db
from app.config import *
from app.models import *

localHost = "http://127.0.0.1:5000/"

class SeleniumTests(unittest.TestCase):
    def setUp(self):
        testApplication = create_application(TestingConfig)
        self.app_context = testApplication.app_context()
        self.app_context.push()
        db.create_all()

        self.server_thread = multiprocessing.Process(target=testApplication.run)
        self.server_thread.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)

        return super().setUp()
    
    def test_homepage(self):
        self.driver.get(localHost)
        self.assertIn("https://127.0.0.1:5000/", self.driver.current_url)

    def tearDown(self):
        self.server_thread.terminate()
        self.driver.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        return super().tearDown()
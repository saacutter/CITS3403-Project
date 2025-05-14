import unittest
from app import db, application
from app.models import Users, Tournaments, Friends
from werkzeug.security import generate_password_hash

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        application.config['TESTING'] = True
        self.app_context = application.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()




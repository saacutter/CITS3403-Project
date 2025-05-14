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

def test_user_creation(self):
    user = Users(username='testuser', email='test@example.com', password='hashed', profile_picture='pic.png', private=True)
    db.session.add(user)
    db.session.commit()
    self.assertEqual(Users.query.count(), 1)


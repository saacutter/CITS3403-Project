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
        user = Users(username='testuser1', email='testuser@example.com', password='hashed', profile_picture='picture.png', private=True)
        db.session.add(user)
        db.session.commit()
        self.assertEqual(Users.query.count(), 1)

    def test_check_password(self):
        password = 'testpassword'
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        user = Users(username='testuser2', email='testuser2@example.com', password=hashed_pw, profile_picture='pic2.png', private=False)
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.check_password(password))

    def test_is_friends_with(self):
        user1 = Users(username='isaac', email='isaac@example.com', password='123456', profile_picture='pic1.png', private=False)
        user2 = Users(username='jordan', email='jordan@example.com', password='789', profile_picture='pic2.png', private=False)
        db.session.add_all([user1, user2])
        db.session.commit()

        friend = Friends(from_user=user2.id, to_user=user1.id)
        db.session.add(friend)
        db.session.commit()

        self.assertTrue(user1.is_friends_with(user2))

    def test_tournament_creation(self):
        user = Users(username='admin', email='admin@example.com', password='hashed', profile_picture='admin.png', private=False)
        db.session.add(user)
        db.session.commit()
        tournament = Tournaments(user_id=user.id, name='Chess Championship', game_title='Chess', date='2025-05-14', points=3, result='win', details='Final round')
        db.session.add(tournament)
        db.session.commit()
        self.assertEqual(Tournaments.query.count(), 1)

    def test_add_friend(self):
        user1 = Users(username='arnav', email='arnav@example.com', password='pw1', profile_picture='arnav1.png', private=False)
        user2 = Users(username='jay', email='jay@example.com', password='pw2', profile_picture='jay1.png', private=False)
        db.session.add_all([user1, user2])
        db.session.commit()

        friend = Friends(from_user=user1.id, to_user=user2.id)
        db.session.add(friend)
        db.session.commit()

        self.assertEqual(Friends.query.count(), 1)
        self.assertEqual(Friends.query.first().from_user, user1.id)
        self.assertEqual(Friends.query.first().to_user, user2.id)
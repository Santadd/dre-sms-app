import unittest
from app.models import User, Permission, Role, AnonymousUser
from app import db, create_app
import time


#unit tests for password hashing functionality
class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)
        
    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password
            
    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))
        
    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)
        
    def test_valid_confirmation_token(self):
        u = User(password='cat', email='santa@email.com', first_name='Abc', last_name='cde', username='buye')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u1 = User(password='cat', email='santa@email.com', first_name='Abc', last_name='cde', username='buye')
        u2 = User(password='dog', email='santsa@email.com', first_name='acabc', last_name='cde', username='eabuye')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = User(password='cat', email='santa@email.com', first_name='Abc', last_name='cde', username='buye')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))
        
    def test_user_role(self):
        u = User(password='cat', email='santa@email.com', first_name='Abc', last_name='cde', username='buye')
        self.assertTrue(u.can(Permission.READ))
        self.assertTrue(u.can(Permission.EDIT))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_moderator_role(self):
        r = Role.query.filter_by(name='Moderator').first()
        u = User(password='cat', email='santa@email.com', first_name='Abc', last_name='cde', username='buye', role=r)
        self.assertTrue(u.can(Permission.READ))
        self.assertTrue(u.can(Permission.EDIT))
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_administrator_role(self):
        r = Role.query.filter_by(name='Administrator').first()
        u = User(password='cat', email='santa@email.com', first_name='Abc', last_name='cde', username='buye', role=r)
        self.assertTrue(u.can(Permission.READ))
        self.assertTrue(u.can(Permission.EDIT))
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertTrue(u.can(Permission.ADMIN))
        
    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.READ))
        self.assertFalse(u.can(Permission.EDIT))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))
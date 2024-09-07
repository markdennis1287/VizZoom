import unittest
from app import app, db
from app.models import User

class TestRoutes(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home(self):
        with self.app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.app.post('/register', data=dict(
            username='testuser',
            email='test@test.com',
            password='password',
            confirm_password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        user = User(username='testuser', email='test@test.com', password='password')
        db.session.add(user)
        db.session.commit()
        response = self.app.post('/login', data=dict(
            email='test@test.com',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()


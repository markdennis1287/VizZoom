import unittest
from app import app
from app import db
from app.models import User, Dataset

class TestModels(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_creation(self):
        user = User(username='testuser', email='test@test.com', password='password')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(User.query.count(), 1)

    def test_dataset_creation(self):
        user = User(username='testuser', email='test@test.com', password='password')
        db.session.add(user)
        db.session.commit()
        dataset = Dataset(name='test.csv', user_id=user.id)
        db.session.add(dataset)
        db.session.commit()
        self.assertEqual(Dataset.query.count(), 1)

if __name__ == '__main__':
    unittest.main()


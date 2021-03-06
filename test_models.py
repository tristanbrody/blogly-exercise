from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Tests user model on mini-app for Blogly exercise"""

    def setUp(self):
        User.query.delete()

    def tearDown(self):
        db.session.rollback()
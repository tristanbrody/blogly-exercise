from unittest import TestCase
from app import app
from flask import url_for

app.config['TESTING'] = True

class RoutingTestCase(TestCase):
    """Testing view functions in main app"""
    def setUp(self):
        self.app = app.test_client()

    def test_users_page(self):
        """Test get requests to users page, and redirects to users page from root"""
        with self.app:
            response = self.app.get(url_for('list_users'))
            self.assertEqual(response.status_code, 200)
            response = self.app.get(url_for('home'), follow_redirects=True)
            self.assertEqual(response.location, 'http://127.0.0.1:5000/users')
    
    # def test_new_users_page(self):
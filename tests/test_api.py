"""
Basic API endpoint tests
"""
import unittest
from app import app

class TestAPI(unittest.TestCase):
    """Test API endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_homepage(self):
        """Test homepage loads"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_dashboard(self):
        """Test dashboard loads"""
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_api_dashboard_stats(self):
        """Test dashboard stats API"""
        response = self.app.get('/api/dashboard/stats')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('stats', data)

if __name__ == '__main__':
    unittest.main()


import unittest
from app import create_app

class TestUserAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()

    def test_multiple_get_requests(self):
        # Existing user
        for _ in range(10):
            response = self.app.get('/user/1')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['id'], 1)

        # Non-existing user
        for _ in range(2):
            response = self.app.get('/user/999')
            self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()

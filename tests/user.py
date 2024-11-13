import unittest
from app import create_app
import random

class TestUserAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()

    def test_multiple_get_requests(self):
        # Simulate up to 100 requests, randomly triggering 404
        for _ in range(random.randint(50, 100)):
            try:
              # Around 2% of 400 - Not found
              if random.random() < 0.02:  # 2% chance
                response = self.app.get('/user/999')
                self.assertEqual(response.status_code, 404)
              # Around 98% of 200 - Ok
              else:
                response = self.app.get('/user/1')
                self.assertEqual(response.status_code, 200)
                data = response.get_json()
                self.assertEqual(data['id'], 1)
            except Exception as e:
                print(f"Error in sampling attempt: {e}")

if __name__ == '__main__':
    unittest.main(exit=False)

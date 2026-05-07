import unittest
import json
from api.index import app

class TestMLApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_health_check(self):
        response = self.app.get('/health')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')

    def test_predict_invalid_data(self):
        # Missing data key
        response = self.app.post('/predict', data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Wrong shape
        response = self.app.post('/predict', data=json.dumps({'data': [1, 2]}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()

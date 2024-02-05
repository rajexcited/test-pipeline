import unittest
from ..api import app


class HelloWorldTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get(self):
        # Given
        # When
        response = self.app.get('/')
        # Then
        self.assertEqual(str, type(response.json['hello']))
        self.assertEqual("world", response.json['hello'])
        self.assertEqual(200, response.status_code)

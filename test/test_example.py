#  standard imports
# third party imports
from test.test_base import TestBase


class TestExample(TestBase):

    def test_application_started(self):
        expected_response = b'Welcome to the microservice!'
        actual_esponse = self.test_app.get('/').data
        assert expected_response in actual_esponse

    def test_example_route_returns_status_ok(self):
        expected_response = '200 OK'
        actual_response = self.test_app.get('/routes').status
        self.assertEqual(expected_response, actual_response)

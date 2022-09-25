#  standard imports
import os
# third party imports
import unittest
import app


class TestBase(unittest.TestCase):
    def setUp(self):
        app.App.testing = True
        self.test_app = app.App.test_client()


if __name__ == '__main__':
    unittest.main()

import unittest
import json
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from app import api_up
from app.models.files import drop_files

class TestFilesAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        drop_files()

    @classmethod
    def tearDownClass(cls):
        drop_files()

    def setUp(self):
        # Prepare test client
        self.app = api_up()
        self.client = self.app.test_client

    def test_fetch_files(self):
        bucket = 'hola.amigo.como.estas'
        response = self.client().get('/files/fetch/' + bucket + '/all')
        rsp = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(rsp) is 2)

    def test_fetch_file(self):
        file_name = 'text.txt'
        bucket = 'hola.amigo.como.estas'
        response = self.client().get('/files/fetch/' + bucket + '/' + file_name)
        rsp = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(rsp['success'] is True)

    def test_files_info_all(self):
        response = self.client().get('/files/info_all')
        rsp = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        print len(rsp)
        self.assertTrue(len(rsp) >= 2)

    def test_file_info(self):
        file_name = 'text.txt'
        response = self.client().get('/files/info/' + file_name)
        rsp = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(rsp) is 1)


if __name__ == '__main__':
    unittest.main()

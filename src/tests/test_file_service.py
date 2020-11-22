from ..app.services.file_service import *
import unittest
import json
import inspect


class TestFileService(unittest.TestCase):

    def test_fetch_fail(self):
        file_name = 'test'
        bucket = 'test'
        response = s3_fetch_file(file_name, bucket)
        self.assertFalse(response['success'])

    def test_fetch_success(self):
        file_name = 'text.txt'
        bucket = 'hola.amigo.como.estas'
        response = s3_fetch_file(file_name, bucket)
        self.assertTrue(response['success'])

    def test_fetch_all_success(self):
        bucket = 'hola.amigo.como.estas'
        response = s3_fetch_files(bucket)
        rsp_dict = json.loads(response)
        self.assertTrue(len(rsp_dict) is 2 and rsp_dict[0]['success'] is True and rsp_dict[1]['success'] is True)

    def test_fetch_all_fail(self):
        bucket = 'non.existing.bucket'
        response = s3_fetch_files(bucket)
        self.assertFalse(response['success'])

    def test_get_file_info_success(self):
        file_name = 'text.txt'
        bucket = 'hola.amigo.como.estas'

        # Make sure it will exist
        s3_fetch_file(file_name, bucket)

        response = get_files_info({'file_name': file_name})
        rsp_dict = json.loads(response)
        self.assertTrue(len(rsp_dict) == 1)

    def test_get_file_info_fail(self):
        file_name = 'non_existing_file_name'
        response = get_files_info({'file_name': file_name})
        rsp_dict = json.loads(response)
        self.assertTrue(len(rsp_dict) == 0)

    def test_get_file_info_all(self):
        bucket = 'hola.amigo.como.estas'
        s3_fetch_files(bucket)
        response = get_files_info({})
        rsp_dict = json.loads(response)
        self.assertTrue(len(rsp_dict) > 0)

    def test_calculate_file_hash_fail(self):
        file_path = 'non/existing/path/text.txt'
        response = calculate_file_hash(file_path)
        self.assertFalse(response)

    def test_calculate_file_hash_success(self):
        current_file_path = inspect.getfile(inspect.currentframe())
        response = calculate_file_hash(current_file_path)
        self.assertFalse(not response)


if __name__ == '__main__':
    unittest.main()

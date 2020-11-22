from ..app.models.files import *
import unittest
import json


class TestFileModel(unittest.TestCase):
    def setUp(self):
        drop_files()

    def test_insert_file_info_fail(self):
        file_name = 'text.txt'
        response = insert_file_info(False, file_name, False)
        self.assertFalse(response)

    def test_insert_file_info_success(self):
        file_name = 'test_name'
        file_hash = 'test_hash'
        file_s3_bucket = 'test_bucket'

        response = insert_file_info(file_s3_bucket, file_name, file_hash)
        self.assertTrue(response)

    def test_find_file_success(self):
        # Prepare file
        file_name = 'test_name'
        file_hash = 'test_hash'
        file_s3_bucket = 'test_bucket'
        insert_file_info(file_s3_bucket, file_name, file_hash)

        found = find_file({'file_name': file_name, 'file_S3_bucket': file_s3_bucket, 'file_hash': file_hash})
        rsp_dict = json.loads(found)
        self.assertTrue(len(rsp_dict) is 1)

    def test_find_file_fail(self):
        # Make sure it exist
        file_name = 'test_name_non_existing'
        found = find_file({'file_name': file_name})
        rsp = json.loads(found)
        self.assertTrue(len(rsp) is 0)

    def test_generate_query_empty(self):
        response = generate_query({})
        self.assertFalse(response)

    def test_generate_query_with_args(self):
        query_sent = {'file_name': 'test'}
        query_rsp = generate_query(query_sent)
        self.assertEqual(query_sent, query_rsp)


if __name__ == '__main__':
    unittest.main()

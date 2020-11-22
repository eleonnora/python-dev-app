from ..models import insert_file_info, find_file, update_file_info
from hashlib import md5
from os import path, remove
from boto3 import resource
from botocore import exceptions
from uuid import uuid1
from bson.json_util import dumps
import pathlib
from datetime import datetime

s3 = resource('s3')


# API

# Fetch all the available files within bucket
def s3_fetch_files(bucket_name):
    response = []
    if bucket_name is None:
        return build_error_response('Missing bucket name!')

    try:
        bucket = s3.Bucket(bucket_name)
        # Iterate through all the files within bucket
        for obj in bucket.objects.all():
            # Fetch and process one file from the bucket
            file_info = s3_fetch_file(obj.key, bucket_name)
            response.append(file_info)

        # Return a list containing all fetched file names and hashes
        return dumps(response)
    except exceptions.ClientError:
        return build_error_response('Failed to fetch s3 resources.')


# Fetch and process the file from bucket
def s3_fetch_file(file_name, bucket_name):
    if bucket_name is None:
        return build_error_response('Missing bucket name!')

    # Generate temporary file path
    tmp_file_path = str(pathlib.Path().absolute()) + '/' + file_name + '_' + str(uuid1())

    try:
        bucket = s3.Bucket(bucket_name)
        # Download the file and place it at tmp_file_path
        bucket.download_file(file_name, tmp_file_path)
        print 's3_fetch_file:: File downloaded: ', tmp_file_path

        response = store_file_info(file_name, tmp_file_path, bucket_name)
        print 's3_fetch_file:: File info stored:', response['success']

        # Remove temporary file
        remove(tmp_file_path)

        if not response['success']:
            print 'WARNING: File info insertion failed!'
            return build_error_response('File info insertion failed!')
        else:
            return build_success_response(response['data'])

    except exceptions.ClientError:
        return build_error_response('Fetching file failed, not found.')
    except exceptions.ParamValidationError:
        return build_error_response('Fetching file failed, invalid arguments.')


# Get stored files info
def get_files_info(query):
    response = find_file(query)
    if not response:
        return 'Getting files info failed.'

    return response

##############################################################################
# Helpers


def store_file_info(file_name, tmp_file_path, bucket_name):
    # Calculate file hash
    file_hash = calculate_file_hash(tmp_file_path)
    if not file_hash:
        return build_error_response('File does not exist.')

    file_info = {'file_S3_bucket': bucket_name, 'file_name': file_name, 'file_hash': file_hash}

    print 'store_file_info:: Try to find file info'
    # Check if the file exists
    data = find_file(file_info)
    if not data:
        return build_error_response('Verifying if file info exist failed.')

    # Insert validation flag
    success = None

    # If exists, only update the updated timestamp
    # Data is a string. If it is empty, it will be [], so the len of empty data will be 2.
    if len(data) > 2:
        success = update_file_info(file_info, {'updated': datetime.now()})
    else:
        success = insert_file_info(bucket_name, file_name, file_hash)

    return {'success': success, 'data': {'file_name': file_name, 'file_hash': file_hash}}


# Calculate file hash
def calculate_file_hash(file_path):
    if not path.exists(file_path):
        return False

    file_hash = md5(open(file_path, 'rb').read()).hexdigest()
    return file_hash


def build_error_response(error):
    return {'success': False, 'error': error}


def build_success_response(data):
    return {'success': True, 'data': data}


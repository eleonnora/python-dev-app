from ..models import insert_file_info, find_file, update_file_info
from hashlib import md5
from os import path, remove
from boto3 import resource
from botocore import exceptions
from uuid import uuid1
from bson.json_util import dumps
import pathlib
from datetime import datetime

from .. import constants

s3 = resource('s3')
bucket = s3.Bucket(constants.BUCKET_NAME)


# Fetch all the available files within bucket
def s3_fetch_files():
    response = []
    # Iterate through all the files within bucket
    for obj in bucket.objects.all():
        # Fetch and process one file from the bucket
        file_info = s3_fetch_file(obj.key)
        response.append(file_info)

    # Return a list containing all fetched file names and hashes
    return dumps(response)


# Fetch and process the file from bucket
def s3_fetch_file(file_name):
    # Generate temporary file path
    tmp_file_path = str(pathlib.Path().absolute()) + '/' + file_name + '_' + str(uuid1())

    try:
        # Download the file and place it at tmp_file_path
        bucket.download_file(file_name, tmp_file_path)
        response = store_file_info(file_name, tmp_file_path)

        # Remove temporary file
        remove(tmp_file_path)

        if not response['success']:
            print 'WARNING: File info insertion failed!'
            return build_error_response('File info insertion failed!')
        else:
            return build_success_response(response['data'])

    except exceptions.ClientError as error:
        return build_error_response('Fetching file failed, not found.')
    except exceptions.ParamValidationError as error:
        return build_error_response('Fetching file failed, invalid arguments.')


def store_file_info(file_name, tmp_file_path):
    # Calculate file hash
    file_hash = calculate_file_hash(tmp_file_path)
    if not file_hash:
        return build_error_response('File does not exist.')

    file_info = {'file_S3_bucket': constants.BUCKET_NAME, 'file_name': file_name, 'file_hash': file_hash}

    # Check if the file exists
    data = find_file(file_info)

    # Insert validation flag
    success = True

    # If exists, only update the updated timestamp
    # Data is a string. If it is empty, it will be [], so two len of empty data will be 2.
    if len(data) > 2:
        update_file_info(file_info, {'updated': datetime.now()})
    else:
        success = insert_file_info(constants.BUCKET_NAME, file_name, file_hash)

    return {'success': success, 'data': {'file_name': file_name, 'file_hash': file_hash}}


# Calculate file hash
def calculate_file_hash(file_path):
    if not path.exists(file_path):
        return False

    file_hash = md5(open(file_path, 'rb').read()).hexdigest()
    return file_hash


def build_error_response(error):
    return {'success': 'false', 'error': error}


def build_success_response(data):
    return {'success': 'true', 'data': data}


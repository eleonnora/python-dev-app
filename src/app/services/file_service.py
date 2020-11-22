from ..models import insert_file_info, find_file, update_file_info
from hashlib import md5
from os import path, remove
from boto3 import resource, Session
from botocore import exceptions
from uuid import uuid1
from bson.json_util import dumps
import pathlib
from datetime import datetime
from ..settings import SECRET, ACCESS_KEY, REGION_NAME, DB_HOST

session = Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET,
    region_name=REGION_NAME
)

s3 = session.resource('s3')

"""

Fetches all the available files within given bucket.

bucket_name - Bucket name

returns:

Success: list of fetched files with success status, file name and hash data:
[{
    'success': boolean,
    'data': {'file_name': file_name, 'file_hash': file_hash}
}, ... ]

Fail: dict with falsy success status and error message:
{
    'success': boolean,
    'error': string
}
"""


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


"""

Fetches and processes the file from the given bucket.

file_name - File name to be fetched
bucket_name - Bucket name

Success: dict with success status, file name and hash data:
{
    'success': boolean,
    'data': {'file_name': file_name, 'file_hash': file_hash}
}

Fail: dict with falsy success status and error message:
{
    'success': boolean,
    'error': string
}
"""


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


"""

Gets file info stored in DB.

query - Dict containing none, one or more of: file_name, file_s3_bucket, file_hash

returns found data or error message if fails
"""


def get_files_info(query):
    response = find_file(query)
    if not response:
        return build_error_response('Getting files info failed.')

    return build_success_response(response)

##############################################################################
# Helpers


"""

Method calculates file hash and stores appropriate info in DB.

file_name - File name
tmp_file_path - Temporary file path to which file will be download in order to be processed
bucket_name - Bucket name

returns:

Success: dict with success status, file name and hash data:
{
    'success': boolean,
    'data': {'file_name': file_name, 'file_hash': file_hash}
}
Fail: dict with falsy success status and error message:
{
    'success': boolean,
    'error': string
}
"""


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


"""

Calculates hash of file on given path.

file_path - file for which hash should be calculated

returns False if file does not exist, otherwise returns calculated hash
"""


def calculate_file_hash(file_path):
    if not path.exists(file_path):
        return False

    file_hash = md5(open(file_path, 'rb').read()).hexdigest()
    return file_hash


def build_error_response(error):
    return {'success': False, 'error': error}


def build_success_response(data):
    return {'success': True, 'data': data}


from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from datetime import datetime
from bson.json_util import dumps
from .. import constants
from ..settings import DB_HOST

client = None
db = None

# Field names which exist in DB collection
FILE_NAME = 'file_name'
HASH = 'hash'
CREATED = 'created'
UPDATED = 'updated'
FILE_S3_BUCKET = 'file_S3_bucket'

# Dict DB document holder
FILE_COLLECTION = {
    'file_S3_bucket': '',
    'file_name': '',
    'hash': '',
    'created': '',
    'updated': ''
}

db_url = 'mongodb://' + DB_HOST + ':27017/'

try:
    # Create connection to MongoDB
    client = MongoClient(db_url)
    # Use db named DB_NAME
    db = client[constants.DB_NAME]
except ConnectionFailure:
    print("Mongo Server not available on url: ", db_url)
    exit(-1)


"""
Finds file or files in DB with given query arguments.

query_arguments - Dict containing none, one or more of: file_name, file_s3_bucket, file_hash

returns found data or False if connection fails
"""


def find_file(query_arguments):
    # Generate query based on arguments
    query = generate_query(query_arguments)

    try:
        cursor = db[constants.COLL_NAME].find(query)
        json_data = dumps(cursor)
        return json_data
    except ServerSelectionTimeoutError:
        print 'find_file:: server connection timeout'
        return False


"""
Verifies passed arguments and generates appropriate query.

arguments - Dict containing none, one or more of: file_name, file_s3_bucket, file_hash

return prepared query
"""


def generate_query(arguments):
    query = {}

    if FILE_NAME in arguments:
        query[FILE_NAME] = arguments[FILE_NAME]

    if FILE_S3_BUCKET in arguments:
        query[FILE_S3_BUCKET] = arguments[FILE_S3_BUCKET]

    if HASH in arguments:
        query[HASH] = arguments[HASH]

    return query


"""
Inserts/creates new document based on provided info.

file_s3_bucket - Bucket name
file_name - File name
file_hash - File hash

returns True if insertion succeed, False if it fails
"""


def insert_file_info(file_s3_bucket, file_name, file_hash):
    if not file_s3_bucket:
        print 'insert_file_info: Missing param: file_s3_bucket'
        return False

    if not file_name:
        print 'insert_file_info: Missing param: file_name'
        return False

    if not file_hash:
        print 'insert_file_info: Missing param: file_hash'
        return False

    timestamp = datetime.now()

    file_collection = dict(FILE_COLLECTION)

    file_collection[FILE_S3_BUCKET] = file_s3_bucket
    file_collection[FILE_NAME] = file_name
    file_collection[HASH] = file_hash
    file_collection[CREATED] = timestamp
    file_collection[UPDATED] = timestamp

    try:
        db[constants.COLL_NAME].insert(file_collection)
        return True
    except ServerSelectionTimeoutError:
        print 'insert_file_info:: server connection timeout'
        return False


"""

Updates file document with provided info based on query arguments.

query_arguments - Dict containing none, one or more of: file_name, file_s3_bucket, file_hash
update_fields - Fields to be updated in found document

returns True if update succeed, False if it fails
"""


def update_file_info(query_arguments, update_fields):
    query = generate_query(query_arguments)

    try:
        db[constants.COLL_NAME].update_one(query, {'$set': update_fields})
        return True
    except ServerSelectionTimeoutError:
        print 'update_file_info:: server connection timeout'
        return False


"""
Drops collection named COLL_NAME

returns True if drop succeed, False if it fails
"""


def drop_files():
    try:
        return db[constants.COLL_NAME].drop()
    except ServerSelectionTimeoutError:
        print 'update_file_info:: server connection timeout'
        return False

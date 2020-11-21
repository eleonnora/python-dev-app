from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime
from bson.json_util import dumps
from .. import constants

client = None
db = None

FILE_NAME = 'file_name'
HASH = 'hash'
CREATED = 'created'
UPDATED = 'updated'
FILE_S3_BUCKET = 'file_S3_bucket'

FILE_COLLECTION = {
    'file_S3_bucket': '',
    'file_name': '',
    'hash': '',
    'created': '',
    'updated': ''
}

try:
    # Create connection
    client = MongoClient(constants.DB_URL)
    # Use db named DB_NAME
    db = client[constants.DB_NAME]
except ConnectionFailure:
    print("Mongo Server not available on url: ", constants.DB_URL)
    exit(-1)


# Find file in DB with given query arguments
def find_file(query_arguments):
    # Generate query based on arguments
    query = generate_query(query_arguments)

    cursor = db[constants.COLL_NAME].find(query)
    json_data = dumps(cursor)

    return json_data


def generate_query(arguments):
    query = {}

    if FILE_NAME in arguments:
        query[FILE_NAME] = arguments[FILE_NAME]

    if FILE_S3_BUCKET in arguments:
        query[FILE_S3_BUCKET] = arguments[FILE_S3_BUCKET]

    if HASH in arguments:
        query[HASH] = arguments[HASH]

    return query


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

    db[constants.COLL_NAME].insert(file_collection)
    return


# Update file info based on query arguments and with update_fields
def update_file_info(query_arguments, update_fields):
    query = generate_query(query_arguments)
    db[constants.COLL_NAME].update_one(query, {'$set': update_fields})

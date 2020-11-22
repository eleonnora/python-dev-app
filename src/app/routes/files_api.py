from flask import Blueprint
from ..services import s3_fetch_file, s3_fetch_files, get_files_info


files_blueprint = Blueprint('files_blueprint', __name__)


@files_blueprint.route('/fetch/<bucket_name>', methods=['GET'])
def fetch_files(bucket_name):
    print 's3_fetch_files invoke'
    files = s3_fetch_files(bucket_name)
    return files


@files_blueprint.route('/fetch/<bucket_name>/<file_name>', methods=['GET'])
def fetch_file(bucket_name, file_name):
    print 's3_fetch_file invoke'
    location = s3_fetch_file(file_name, bucket_name)
    return location


@files_blueprint.route('/info', methods=['GET'])
def fetch_all_files_info():
    print 'get_files_info all invoke'
    files_info = get_files_info({})
    return files_info


@files_blueprint.route('/info/<file_name>', methods=['GET'])
def fetch_file_info(file_name):
    print 'get_files_info invoke'
    file_info = get_files_info({'file_name': file_name})
    return file_info

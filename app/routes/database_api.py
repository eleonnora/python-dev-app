from flask import Blueprint, request
from ..models import find_file

db_blueprint = Blueprint('db_blueprint', __name__)


@db_blueprint.route('/<file_name>', methods=['GET'])
def fetch_file_info(file_name):
    print "fetch_file_info"
    file_info = find_file({'file_name': file_name})
    return file_info


@db_blueprint.route('/all', methods=['GET'])
def fetch_all_files_info():
    print "fetch_all_files_info"
    files_info = find_file({})
    return files_info

from flask import Blueprint
from ..services import s3_fetch_file, s3_fetch_files


files_blueprint = Blueprint('files_blueprint', __name__)


@files_blueprint.route('/all', methods=['GET'])
def fetch_files():
    files = s3_fetch_files()
    return files


@files_blueprint.route('/<file_name>', methods=['GET'])
def fetch_file(file_name):
    print(file_name)
    location = s3_fetch_file(file_name)
    return location


from flask import Flask
from routes import files_blueprint, db_blueprint
from services import s3_fetch_file, s3_fetch_files
from models import find_file


def api_up():
    print 'api_up:: Run API.'
    app = Flask(__name__)
    # Register fetching files and populating data API
    app.register_blueprint(files_blueprint, url_prefix='/files/fetch')
    # Register fetching populated file data api
    app.register_blueprint(db_blueprint, url_prefix='/files/info')

    app.run()
    return


def app_cli(args):
    print 'app_cli:: Start CLI.'

    if args['fetch_file']:
        location = s3_fetch_file(args['fetch_file'])
        return location

    if args['fetch_all']:
        location = s3_fetch_files()
        return location

    if args['stored_file_info']:
        file_info = find_file({'file_name': args['stored_file_info']})
        return file_info

    if args['stored_file_info_all']:
        all_files_info = find_file({})
        return all_files_info

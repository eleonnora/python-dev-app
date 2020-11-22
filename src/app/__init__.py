from flask import Flask
from routes import files_blueprint
from services import s3_fetch_file, s3_fetch_files, get_files_info


def api_up():
    print 'api_up:: Run API.'
    app = Flask(__name__)
    # Register fetching files and populating data API
    app.register_blueprint(files_blueprint, url_prefix='/files')
    app.run()

    @app.errorhandler(404)
    def page_not_found():
        return 'This page does not exist', 404

    return app


def app_cli(args):
    print 'app_cli:: Start CLI.'

    if args['fetch_file']:
        location = s3_fetch_file(args['fetch_file'], args['bucket'])
        return location

    if args['fetch_all']:
        location = s3_fetch_files(args['bucket'])
        return location

    if args['stored_file_info']:
        file_info = get_files_info({'file_name': args['stored_file_info']})
        return file_info

    if args['stored_file_info_all']:
        all_files_info = get_files_info({})
        return all_files_info

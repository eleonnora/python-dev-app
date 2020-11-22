from argparse import ArgumentParser
from app import api_up, app_cli

if __name__ == '__main__':
    # Construct the argument parser
    ap = ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument('-b', '--bucket', required=False,
                    help='Bucket name.')
    ap.add_argument('-ff', '--fetch_file', required=False,
                    help='File name to be downloaded.')
    ap.add_argument('-ffa', '--fetch_all', required=False,
                    help='Download all files',
                    action='store_true')
    ap.add_argument('-sfi', '--stored_file_info', required=False,
                    help='Get file info from DB.')
    ap.add_argument('-sfia', '--stored_file_info_all', required=False,
                    help='Get all files info from DB.',
                    action='store_true')

    args = vars(ap.parse_args())

    # The arguments are exclusive. Truthy can be one and only one (without bucket name).
    ff = args['fetch_file'] is not None
    sfi = args['stored_file_info'] is not None
    if [ff, args['fetch_all'], sfi, args['stored_file_info_all']].count(True) > 1:
        print 'Cannot use more than one argument!'
        exit(-1)

    cmd_args = args['fetch_file'] or args['fetch_all'] or args['stored_file_info'] or args['stored_file_info_all']

    if cmd_args:
        response = app_cli(args)
        print '\n Response: \n\n', response, '\n'
    else:
        api_up()


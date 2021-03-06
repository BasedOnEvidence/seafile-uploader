import argparse


def get_args_parser():
    doc_link = 'https://download.seafile.com/published/web-api/home.md'
    parser = argparse.ArgumentParser(description='Seafile file uploader')
    parser.add_argument('server',
                        help='set seafile server (e.g. https://cloud.seafile.com)')
    parser.add_argument('filepath',
                        help='set path to file to upload')
    parser.add_argument('-t',
                        '--token',
                        default=None,
                        help='set token, for more information check {}'.format(
                            doc_link)
                        )
    parser.add_argument('-l',
                        '--login',
                        default=None,
                        help='set login for auth in seafile server, default None')
    parser.add_argument('-p',
                        '--password',
                        default=None,
                        help='set password for auth in seafile server, default None')
    parser.add_argument('-r',
                        '--reponame',
                        default='Default-repo',
                        help='set repository name, default: Default-repo')
    parser.add_argument('-ri',
                        '--repoid',
                        default=None,
                        help='set repository id, default None')
    parser.add_argument('-ul',
                        '--uploadurl',
                        default=None,
                        help='set upload url, default None')
    parser.add_argument('-rp',
                        '--repopath',
                        default='/',
                        help='set path in repository, default: /')
    parser.add_argument('-fp',
                        '--fpassword',
                        default=None,
                        help='set password to file, no password is set by default')
    parser.add_argument('-fe',
                        '--fexpiration',
                        default=None,
                        help='set link expiration in days, no expiration by default')

    return parser

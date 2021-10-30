import re
import requests
import getpass
from uploader.api import _get_upload_link


def main():
    server = input('Enter the server (e.g. https://cloud.seafile.com): ')
    username = input('Enter username (e.g. username@example.com): ')
    password = getpass.getpass('Enter password: ')
    data = {
        'username': username,
        'password': password
    }
    if server[-1] == '/':
        server = server[:-1]
    try:
        response = requests.post(server + '/api2/auth-token/', data=data)
        print(response.text)
    except requests.exceptions.RequestException as err:
        print(err)
    token = re.match(r'{"token":"(.*)"}', response.text).group(1)
    repoid = input('Enter repo id (e.g. c506813f-4a1d-4b33-923d-f49a1178834f): ')
    repopath = input('Enter repo path (e.g. /): ')
    try:
        print(_get_upload_link(server, token, repoid, repopath))
    except Exception as err:
        print(err)
    input('Press Enter to continue')


if __name__ == "__main__":
    main()

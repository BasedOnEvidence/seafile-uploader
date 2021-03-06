import requests
import re
import json
import getpass
from uploader.utils import urljoin
from uploader.logger import get_logger

logger = get_logger(__name__)


def get_repo_list(server, token):
    headers = {
        'Authorization': 'Token {}'.format(token),
        'Accept': 'application/json; indent=4',
    }
    response = requests.get(
        urljoin(server, '/api2/repos/?type=mine'),
        headers=headers
    )
    logger.info('get_repo_list: {}'.format(response.text))
    return json.loads(response.text)


def list_share_links_of_repo(server, token, repo_id):
    headers = {
        'Authorization': 'Token {}'.format(token),
        'Accept': 'application/json; charset=utf-8; indent=4',
    }
    params = (
        ('repo_id', repo_id),
    )
    response = requests.get(
        urljoin(server, '/api/v2.1/share-links/?repo_id=', repo_id),
        headers=headers, params=params
    )
    logger.info('list_share_links_of_repo: {}'.format(response.text))
    return json.loads(response.text)


def create_repo(server, token, repo_name):
    headers = {
        'Authorization': 'Token {}'.format(token),
        'Accept': 'application/json; indent=4',
    }
    data = {
        'name': repo_name
    }
    response = requests.post(
        urljoin(server, '/api2/repos/'),
        headers=headers, data=data
    )
    return json.loads(response.text)


def get_repo(server, token, repo_id):
    headers = {
        'Authorization': 'Token {}'.format(token),
        'Accept': 'application/json; indent=4',
    }
    response = requests.get(
        urljoin(server, '/api2/repos/', repo_id),
        headers=headers
    )
    return json.loads(response.text)


def delete_file(server, token, repo_id, file_path):
    headers = {
        'Authorization': 'Token {}'.format(token),
        'Accept': 'application/json; charset=utf-8; indent=4',
    }
    params = (
        ('p', file_path),
    )
    response = requests.delete(
        urljoin(server, '/api2/repos/', repo_id, '/file/?p=', file_path),
        headers=headers, params=params
    )
    logger.info('delete_file: {}'.format(response.text))
    return response


def delete_share_link(server, token, link_token):
    headers = {
        'Authorization': 'Token {}'.format(token),
    }
    response = requests.delete(
        urljoin(server, '/api/v2.1/share-links/', link_token),
        headers=headers
    )
    logger.info('delete_share_link: {}'.format(response.text))
    return response


def _get_upload_link(server, token, repo_id, repo_path):
    if repo_path == '/':
        repo_path = ''
    elif repo_path[-1] == '/':
        repo_path = repo_path[:-1]
    url_tail = '/api2/repos/{}{}/upload-link/'.format(repo_id, repo_path)
    url = urljoin(server, url_tail)
    logger.info('Current url: {}'.format(url))
    headers = {
        'Authorization': 'Token {}'.format(token),
    }
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as err:
        logger.warning(err)
    logger.info('_get_upload_link: {}'.format(response.status_code))
    try:
        result = re.match(r'"(.*)"', response.text).group(1)
    except re.error as err:
        logger.warning(err)
    return result


def upload_file(
    server, token, repo_id, upload_url, repo_path,
    file_name, file_obj, replace=True
):
    if not upload_url:
        upload_url = _get_upload_link(server, token, repo_id, repo_path)
    headers = {
        'Authorization': 'Token {}'.format(token),
    }
    files = {
        'file': (file_name, file_obj),
        'parent_dir': repo_path,
        'replace': 1 if replace else 0,
    }
    if replace:
        links_data = list_share_links_of_repo(server, token, repo_id)
        for link_rec in links_data:
            if (
                link_rec['path'] == repo_path + file_name and
                link_rec['repo_id'] == repo_id
            ):
                delete_share_link(server, token, link_rec['token'])
        delete_file(server, token, repo_id, repo_path+file_name)
    response = requests.post(
        upload_url, headers=headers, files=files
    )
    logger.info('upload_file: {}'.format(response.text))
    return response.text


def get_file(server, token, repo_id, file_path):
    headers = {
        'Authorization': 'Token {}'.format(token),
        'Accept': 'application/json; charset=utf-8; indent=4',
    }
    params = (
        ('p', file_path),
    )
    response = requests.get(
        urljoin(
            server, '/api2/repos/',
            repo_id, '/file/detail/?p=', file_path
        ),
        headers=headers, params=params
    )
    return response.text


def get_share_link(
    server, token, repo_id, file_path,
    password=None, expire_days=None, direct_link=True
):
    headers = {
        'Authorization': 'Token {}'.format(token),
        'Accept': 'application/json; indent=4',
    }
    data = {
        'path': file_path,
        'repo_id': repo_id,
    }
    if password:
        data['password'] = password
    if expire_days:
        data['expire_days'] = expire_days
    response = requests.post(
        urljoin(server, '/api/v2.1/share-links/'),
        headers=headers, data=data
    )
    logger.info('get_share_link: {}'.format(response.text))
    link = json.loads(response.text)['link']
    if direct_link:
        link = link + '?dl=1'
    return link


def get_token(server, username, password):
    if not server:
        server = input('Enter the server (e.g. https://cloud.seafile.com): ')
    if server[-1] == '/':
        server = server[:-1]
    if not username:
        username = input('Enter username (e.g. username@example.com): ')
    if not password:
        max_attempts = 5
        current_attempt_number = 0
    while current_attempt_number < max_attempts:
        password = getpass.getpass('Enter password: ')
        data = {
            'username': username,
            'password': password
        }
        try:
            response = requests.post(server + '/api2/auth-token/', data=data)
        except requests.exceptions.RequestException as err:
            logger.warning(err)
        if 'token' in response.text:
            return re.match(r'{"token":"(.*)"}', response.text).group(1)
        else:
            logger.warning('Unable to login with provided credentials')
            current_attempt_number += 1
    raise Exception('Unable to login with provided credentials')

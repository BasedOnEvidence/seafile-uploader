import requests
import re
import json
from uploader.utils import urljoin
from uninstaller.logger import get_logger

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
    return response


def delete_share_link(server, token, link_token):
    headers = {
        'Authorization': 'Token {}'.format(token),
    }
    response = requests.delete(
        urljoin(server, '/api/v2.1/share-links/', link_token),
        headers=headers
    )
    return response


def _get_upload_link(server, token, repo_id, repo_path):
    url = urljoin(server, '/api2/repos/', repo_id + repo_path, '/upload-link/')
    headers = {
        'Authorization': 'Token {}'.format(token),
    }
    response = requests.get(url, headers=headers)
    return re.match(r'"(.*)"', response.text).group(1)


def upload_file(
    server, token, repo_id, repo_path,
    file_name, file_obj, replace=True
):
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
    link = json.loads(response.text)['link']
    if direct_link:
        link = link + '?dl=1'
    return link

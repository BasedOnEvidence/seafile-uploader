import os
from uploader.api import (
    get_repo_list, create_repo,
    get_repo, upload_file,
    get_share_link
)
from uploader.logger import get_logger

logger = get_logger(__name__)


def upload_local_file(
    server, token, repo_id, upload_url, repo_path,
    file_path, replace=True
):
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as file_obj:
        return (
            upload_file(
                server, token, repo_id, upload_url, repo_path, file_name, file_obj, replace
            ),
            file_name
        )


def get_target_repo(server, token, repo_name):
    logger.info('Looking for library "{}"'.format(repo_name))
    for repo in get_repo_list(server, token):
        if repo['name'] == repo_name:
            return repo
    logger.info('Creating library "{}"'.format(repo_name))
    return get_repo(
        server, token, create_repo(server, token, repo_name)['repo_id']
    )


def upload(
        server, token,
        filepath, reponame, repoid, uploadurl,
        repopath, fpassword, fexpiration
):
    try:
        logger.info('Seafile-uploader started')
        if not repoid:
            repo = get_target_repo(server, token, reponame)
            repoid = repo['id']
        logger.info('Uploading "{}"'.format(filepath))
        _, file_name = upload_local_file(
            server, token, repoid, uploadurl, repopath, filepath
        )
        library_file_path = repopath + file_name
        logger.info('Getting share link of "{}"'.format(library_file_path))
        link = get_share_link(
            server, token, repoid, library_file_path,
            password=fpassword, expire_days=fexpiration
        )
        logger.info('Success: {}'.format(link))
    except Exception as err:
        logger.warning(err)
        return err
    return link

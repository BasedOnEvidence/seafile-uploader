
<h2 align="center">Seafile Uploader</h2>

<p align="center">
  <a href="#descrition">Description</a> •
  <a href="#key-features">Key Features</a> •
  <a href="#download">Download</a> •
  <a href="#build">Build</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>


## Descrition

Program for uploading files to seafile via command line interface. Helps in the automation of uploading.

## Key Features

* The minimum set of required parameters. Just specify server, token and file to upload.
* Allows to make shared links for uploaded files
* Allows to make password protection
* Repo will auto-create if not exists
* There is an auxiliary utility for obtaining a token

## Download

You can [download](https://github.com/BasedOnEvidence/seafile-uploader/releases) the latest installable version of seafile uploader for Windows

## Build

If you want to build .exe yourself, you'll need [Git](https://git-scm.com) and [Python3](https://www.python.org/downloads/) installed on your computer. From your command line:

```powershell
# Clone this repository
$ git clone https://github.com/BasedOnEvidence/seafile-uploader

# Go into the repository
$ cd seafile-uploader

# Install dependencies
$ pip install pyinstaller
$ pip install requests

# Build get-seafile-token.exe, seafile-uploader.exe
$ build.bat
```

If you use Linux, you need to connect package manager to this project. I will show using [Poetry](https://python-poetry.org/docs/#installation) as example.

```bash
# Clone this repository
$ git clone https://github.com/BasedOnEvidence/seafile-uploader

# Go into the repository
$ cd seafile-uploader

# Install dependencies
$ pip install pyinstaller
$ pip install requests

# Install poetry. Set project name, the rest of the settings can be left as default
$ poetry install
```
In pyproject.toml in tool.poetry section add:

```bash
packages = [
  { include = "uploader" },
]
```
In pyproject.toml in tool.poetry.dev-dependencies section add:

```bash
requests = "^2.26.0"
```

In pyproject.toml add new section:

```bash
[tool.poetry.scripts]
seafile-uploader = "uploader.scripts.upload:main"
get-seafile-token = "uploader.scripts.gettoken:main"
```

Now run folowing in terminal:

```bash
#Build project
$ poetry build

#Install packages
$ pip install --user dist/*.whl --force-reinstall
```

Well done, you've installed seafile-uploader and get-seafile-token packages in your system

## How To Use

First you need to get your token. To do this, run get-seafile-token. Insert your seafile server, your login and password. Utility will return token.
You can also enter your repository id and path for future files upload. It's need to upload files with limited permissions (with tokens, wich generated for repos).

Usage: seafile-uploader.exe [-h] [-r REPONAME] [-ri REPOID] [-ul UPLOADURL] [-rp REPOPATH] [-fp FPASSWORD] [-fe FEXPIRATION] server token filepath

Seafile file uploader

positional arguments:<br />
  server                set seafile server (e.g. https://cloud.seafile.com)<br />
  token                 set token, for more information check https://download.seafile.com/published/web-api/home.md<br />
  filepath              set path to file to upload

optional arguments:<br />
  -h, --help            show this help message and exit<br />
  -r REPONAME, --reponame REPONAME
                        set repository name, default: Default-repo<br />
  -ri REPOID, --repoid REPOID
                        set repository id, default None<br />
  -ul UPLOADURL, --uploadurl UPLOADURL
                        set upload url, default None<br />
  -rp REPOPATH, --repopath REPOPATH
                        set path in repository, default: /<br />
  -fp FPASSWORD, --fpassword FPASSWORD
                        set password to file, no password is set by default<br />
  -fe FEXPIRATION, --fexpiration FEXPIRATION
                        set link expiration in days, no expiration by default

## Credits

This software uses the following open source packages:

- [Pyinstaller](https://www.pyinstaller.org/)
- [Requests](https://pypi.org/project/requests/)


## You may also like...

- [Anyconnect uninstaller](https://github.com/BasedOnEvidence/anyconnect-uninstaller) - A program for uninstall cisco anyconnect

## License

MIT

---

> GitHub [@BasedOnEvidence](https://github.com/BasedOnEvidence/) &nbsp;&middot;&nbsp;



import requests
import getpass
import os


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
    os.system('pause')


if __name__ == "__main__":
    main()

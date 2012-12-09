import readline
import sys
import getpass

import crucible
import config

def main():
    conf = config.Config()
    conf.load_from_file()

    crucible_url = get_crucible_url(conf)
    crucible_conn = crucible.Crucible(crucible_url)
    username = get_username(conf)
    auth_token = get_auth_token(conf, crucible_conn, username)
    project_key = get_project_key(conf)

    review_id = create_review(crucible_conn, username, auth_token, project_key)
    print crucible_url + "/cru/" + review_id

def create_review(crucible, username, auth_token, project_key):
    patch = sys.stdin.read()

    parameters = {
        'allow_reviewers_to_join': True,
        'author': username,
        'description': '',
        'name': '',
        'project_key': project_key,
        'patch': patch
    }

    resp = crucible.create_review(auth_token, **parameters)
    #print resp.request.data
    #print resp.text
    return resp.json['permaId']['id']

def get_crucible_url(conf):
    url = conf.get_value('crucible', 'url')
    if url is None:
        url = acquire_crucible_url()
        conf.set_value('crucible', 'url', url)
    return url

def acquire_crucible_url():
    prompt = "Please enter the URL for crucible (probably something like http://hostname.com/fisheye): "
    return raw_input(prompt)

def get_project_key(conf):
    project_key = conf.get_value('crucible', 'project_key')
    if project_key is None:
        project_key = prompt_for_project_key()
        conf.set_value('crucible', 'project_key', project_key)
    return project_key

def prompt_for_project_key():
    prompt = "Please enter your crucible project key (probably something like CR): "
    return raw_input(prompt)

def get_username(conf):
    username = conf.get_value('crucible', 'username')
    if username is None:
        username = prompt_for_username()
        conf.set_value('crucible', 'username', username)
    return username

def prompt_for_username():
    prompt = "Please enter your crucible username: "
    return raw_input(prompt)

def get_auth_token(conf, crucible, username):
    token = conf.get_value('crucible', 'token')
    if token is None:
        token = acquire_auth_token(crucible, username)
        conf.set_value('crucible', 'token', token)
    return token

def acquire_auth_token(crucible, username):
    password = prompt_for_password()
    response = crucible.get_auth_token(username, password)
    return response.json['token']

def prompt_for_password():
    print "In order to get an auth token from crucible, you must enter your password once."
    password = getpass.getpass()
    return password

if __name__ == '__main__':
    sys.exit(main())
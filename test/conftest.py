import os, sys

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')
sys.path.append(ROOT_DIR)


def get_user_id(name):
    return "user_{}_{}".format(len(name), name)


def get_issue_id(org, repo, number, _type="issue"):
    return "{}_{}_{}_{}".format(_type, org, repo, number)


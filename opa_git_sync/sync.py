import json
import logging
import time
import requests

logger = logging.getLogger(__name__)


class HTTPDestination(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def send(self, data):
        data = json.dumps(data)
        response = requests.request(
            method='PUT',
            url=self.base_url,
            data=data,
            headers={'Content-Type': 'application/json'})
        response.raise_for_status()


class StdoutDestination(object):
    def send(self, data):
        s = json.dumps(data, indent=2, sort_keys=True)
        print(s)


def poll(repos):
    data = {}
    for repo in repos.values():
        _, nested = mkdir(repo, data)
        with repo.clone():
            nested['log'] = list(repo.log())
    return data


def one_shot(dest, repos):
    data = poll(repos)
    dest.send(data)


def loop(dest, delay, repos):
    while 1:
        try:
            data = poll(repos)
            dest.send(data)
        except Exception as e:
            logger.exception(e)
        time.sleep(delay)


def mkdir(repo, data):
    """Returns data after mutating it to include data for repo."""
    if repo.hostname:
        repo_data = data.setdefault(repo.hostname, {})
    else:
        repo_data = data
    for part in repo.path:
        repo_data = repo_data.setdefault(part, {})
    return data, repo_data

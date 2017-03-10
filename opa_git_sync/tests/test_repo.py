from opa_git_sync import repo


def test_repo_hostname():
    r = repo.Repo(name='test',
                  url="git@github.com/open-policy-agent/opa.git")
    assert r.hostname == 'github.com'

    r = repo.Repo(name='test',
                  url="https://github.com/open-policy-agent/opa.git")
    assert r.hostname == 'github.com'


def test_repo_path():
    r = repo.Repo(name='test',
                  url="git@github.com/open-policy-agent/opa.git")

    assert r.path == ['open-policy-agent', 'opa']


def test_repo_log():
    r = repo.Repo(name='test', url='file:///src')
    first_commit = 'a875502ecfbb0be197cb23670e92c5606635442b'
    with r.clone():
        all_commits = list(r.log())
        assert all_commits[-1]['commit'] == first_commit

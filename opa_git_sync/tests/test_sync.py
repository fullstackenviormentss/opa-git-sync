from opa_git_sync import repo
from opa_git_sync import sync


def test_mkdir():
    r = repo.Repo(name='test',
                  url="git@github.com/open-policy-agent/opa.git")
    root, nested = sync.mkdir(r, {
        "github.com": {
            "tsandall": {
                "deadbeef": {}
            },
        },
    })
    assert root == {
        "github.com": {
            "tsandall": {"deadbeef": {}},
            "open-policy-agent": {"opa": {}},
        },
    }
    assert nested == {}

    r = repo.Repo(name='test', url='file:///src')
    root, nested = sync.mkdir(r, {})
    assert root == {'src': {}}
    assert nested == {}


def test_poll():
    data = sync.poll({"test": repo.Repo(name='test', url='file:///src')})
    first_commit = 'a875502ecfbb0be197cb23670e92c5606635442b'
    assert data['src']['log'][-1]['commit'] == first_commit

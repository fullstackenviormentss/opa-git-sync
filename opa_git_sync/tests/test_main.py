from opa_git_sync import main


def test_load_repos():
    repos = main.load_repos({
        "OPA_GIT_URL_foo": "git@github.com/open-policy-agent/foo",
        "OPA_GIT_DEPTH_foo": "100",
        "OPA_GIT_URL_bar": "git@github.com/open-policy-agent/bar",
        "OPA_GIT_DEPTH_bar": "200",
        "OPA_GIT_URL_baz": "git@github.com/open-policy-agent/baz",
        "OPA_GIT_DEPTH_baz": "-1",
        "OPA_GIT_URL_qux": "git@github.com/open-policy-agent/qux",
    })
    assert len(repos) == 4
    assert repos['foo'].url == "ssh://git@github.com/open-policy-agent/foo"
    assert repos['foo'].depth == 100
    assert repos['bar'].url == "ssh://git@github.com/open-policy-agent/bar"
    assert repos['bar'].depth == 200
    assert repos['baz'].url == "ssh://git@github.com/open-policy-agent/baz"
    assert repos['baz'].depth is None
    assert repos['qux'].url == "ssh://git@github.com/open-policy-agent/qux"
    assert repos['qux'].depth == main.default_depth

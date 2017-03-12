import contextlib
import git
import shutil
import subprocess
import tempfile
from urllib.parse import urlparse


class Repo(object):
    """Repo provides a simple abstraction around a remote Git repository."""
    def __init__(self, name, url, depth=None):
        self.name = name

        # Normalize the url.
        scheme, _, rest = url.partition('://')
        if not rest:
            self.url = 'ssh://' + url
        else:
            self.url = url

        self.depth = depth

    @contextlib.contextmanager
    def clone(self):
        """Yields context with a local copy of the remote repository.

        Call this before other operations that interact with the repository
        such as log.
        """
        self.dirpath = tempfile.mkdtemp()
        try:
            args = ['git', 'clone', '--quiet', '--bare']
            if self.depth and self.depth >= 1:
                args.extend(['--depth', str(self.depth)])
            args.append(self.url)
            args.append(self.dirpath)
            subprocess.check_call(args)
            yield
        finally:
            shutil.rmtree(self.dirpath)

    def log(self):
        """Yields commit objects."""
        repo = git.Repo(self.dirpath)
        for commit in repo.iter_commits():
            yield {
                'commit': commit.hexsha
            }
        repo.close()

    @property
    def hostname(self):
        """Returns Git repo hostname or None if unset."""
        parsed = urlparse(self.url)
        return parsed.hostname

    @property
    def path(self):
        """Returns Git repo path."""
        parsed = urlparse(self.url)
        return parsed.path.strip('/').rstrip('.git')

import argparse
import logging
import os
import sys
import textwrap
import opa_git_sync
from opa_git_sync import repo
from opa_git_sync import sync

default_depth = 1000
env_prefix = 'OPA_GIT_'


def main(args):
    parser = argparse.ArgumentParser(
        description='Replicate Git repository information into OPA.',
        epilog=textwrap.dedent("""

Overview
========

{prog} replicates Git repository information into OPA. Environment variables
are used to control the Git repostiories that are replicated.

OPA_GIT_URL_<name>=<url> sets the Git repository URL for repository <name>.
This is the URL that {prog} will use to clone the repository.

OPA_GIT_DEPTH_<name>=<depth> sets the number of commits to include for
repository <name>. The default depth is {default_depth}. If the depth is set to
<= 0, the entire repository history will be cloned.

All of these environment variables are grouped by the <name> value. The <name>
value does not affect the location of data pushed into OPA.

Examples
========

"Replicate two repositories, foo and bar, with 100 most recent commits from
each every 30 seconds into document at path /git":

$ export OPA_GIT_URL_foo=git@github.com/example/foo.git
$ export OPA_GIT_DEPTH_foo=100
$ export OPA_GIT_URL_bar=git@github.com/example/bar.git
$ export OPA_GIT_DEPTH_bar=100
$ {prog} --base-url http://localhost:8181/v1/data/git --delay=30

The data for repositories foo and bar would be available at
http://localhost:8181/v1/data/git/github.com/example/foo and
http://localhost:8181/v1/data/git/github.com/example/bar respectively.

Data
====

The repository data is nested under an object at the --base-url:

{{
    <url>: {{        # e.g., github.com/example/foo
      ...
    }}
}}

For each repository {prog} creates an object as follows:

{{
    "log": [
        {{
            "commit": <hash>
        }},
        ...
    ]
}}
""".format(prog=os.path.basename(sys.argv[0]), default_depth=default_depth)),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--one-shot', action='store_true',
                        help='run once and exit')
    parser.add_argument('--delay', action='store', type=int, default=60,
                        help='polling delay in seconds')
    parser.add_argument('--base-url', action='store',
                        default='http://localhost:8181/v1/data/git',
                        help='url of API and base path to data')
    parser.add_argument('--stdout', action='store_true',
                        help='send data to STDOUT instead of API')
    parser.add_argument('--level', choices=['DEBUG', 'INFO', 'ERROR'],
                        help='logging level', default='INFO')
    parser.add_argument('--version', action='store_true',
                        help='print version and exit')

    args = parser.parse_args()
    if args.version:
        print(opa_git_sync.__version__)
        sys.exit(0)

    if args.stdout:
        dest = sync.StdoutDestination()
    else:
        dest = sync.HTTPDestination(args.base_url)

    repos = load_repos(os.environ)
    setup_logging(args.level)

    if args.one_shot:
        sync.one_shot(dest, repos)
    else:
        sync.loop(dest, args.delay, repos)


def load_repos(environ):
    repos = {}
    for k, v in environ.items():
        if k.startswith(env_prefix):
            key, _, name = k[len(env_prefix):].partition('_')
            if not name:
                continue
            repos.setdefault(name, {})[key.lower()] = v
    for name, cfg in repos.items():
        if 'url' not in cfg:
            continue
        depth = int(cfg.get('depth', default_depth))
        if depth <= 0:
            depth = None
        repos[name] = repo.Repo(name=name, url=cfg['url'],
                                depth=depth)
    return repos


def setup_logging(level):
    root = logging.getLogger()
    root.setLevel(level)
    ch = logging.StreamHandler(sys.stderr)
    ch.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

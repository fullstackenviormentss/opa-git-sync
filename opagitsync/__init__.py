import argparse
import os
import sys
import textwrap

__version__ = "0.0.1-dev"


def main(args):
    """entrypoint to the tool."""
    parser = argparse.ArgumentParser(
        description='Replicate Git repository information into OPA.',
        epilog=textwrap.dedent("""

Overview
========

{prog} replicates Git repository information into OPA. Environment variables are
used to control the Git repostiories that are replicated.

OPA_GIT_URL_<name>=<url> sets the Git repository URL for repository <name>. This
is the URL that {prog} will use to clone the repository.

OPA_GIT_DEPTH_<name>=<depth> sets the number of commits to include for
repository <name>. The default depth is 1,000. If the depth is set to <= 0, all
commits will be clonned.

All of these environment variables are grouped by the <name> value. The <name>
value does not affect the location of data pushed into OPA.

Examples
========

"Replicate two repositories, foo and bar, with 100 most recent commits from each
every 30 seconds into document at path /git/example":

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
    <hostname>: {{        # e.g., github.com
       <repo-org>: {{     # e.g., example
         <repo-name>: {{  # e.g., foo
           ...
         }}
       }}
    }}
}}

For each repository {prog} creates an object as follows:

{{
    "log": [
        {{
            "commit": <hash>,
            "author-email": <email>,
            "subject": <subject>
        }},
        ...
    ]
}}
""".format(prog=os.path.basename(sys.argv[0]))),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--one-shot', action='store_true', help='run once and exit')
    parser.add_argument('--delay', action='store', type=int, default=60, help='polling delay in seconds')
    parser.add_argument('--base-url', action='store', default='http://localhost:8181/v1/data/git', help='url of OPA API and base path to data')
    parser.add_argument('--version', action='store_true', help='print version and exit')
    args = parser.parse_args()
    if args.version:
        print(__version__)
        sys.exit(1)

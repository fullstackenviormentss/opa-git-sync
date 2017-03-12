# opa-git-sync

opa-git-sync replicates Git repository information into OPA.

## Building

The project requires Docker to build.

Assuming you have Docker installed, `make` (with no arguments) will:

- Build the Docker image
- Run all of the tests
- Execute flake8 on the code

The resulting Docker image is tagged as `openpolicyagent/opa-git-sync` by default.

## Releasing

During development, the version is set to `{version}-dev`. The Docker image is
not tagged with a version by default.

To produce a release:

- Manually update the `__version__` by removing "-dev" and then commit the
  change.
- Tag the repository with the version: `git tag -a 'v{version}'`.
- Run `make release` to build and tag the image and push to Docker Hub.
- Manually update the `__version__` back to "-dev" for the next release and
  commit the change.

## Running

 See `opa-git-sync --help` for more information.

### Examples

> Replicate two repositories, foo and bar, with 100 most recent commits from
> each every 30 seconds into documents at path /git.

```
$ export OPA_GIT_URL_foo=git@github.com/example/foo.git
$ export OPA_GIT_DEPTH_foo=100
$ export OPA_GIT_URL_bar=git@github.com/example/bar.git
$ export OPA_GIT_DEPTH_bar=100
$ opa-git-sync --base-url http://localhost:8181/v1/data/git --delay=30
```

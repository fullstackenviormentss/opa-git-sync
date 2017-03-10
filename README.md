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
# opa-git-sync

opa-git-sync replicates Git repository information into OPA.

## Building

The project requires Docker to build. Assuming you have Docker installed,
`make` will build the project, run all of the tests, and execute flake8.

The build produces a Docker image that can be deployed:

```
openpolicyagent/opa-git-sync
```
REPO := openpolicyagent/opa-git-sync

all: test

.PHONY: build
build:
	docker build -t $(REPO) .

.PHONY: test
test: build test-unit test-flake8

.PHONY: test-unit
test-unit:
	docker run --rm $(REPO) py.test opa_git_sync

.PHONY: test-flake8
test-flake8:
	docker run --rm $(REPO) flake8

.PHONY: shell
shell: test
	docker run -it --rm $(REPO) bash



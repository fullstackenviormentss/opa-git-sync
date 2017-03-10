IMAGE := openpolicyagent/opa-git-sync
VERSION := $(shell python -c 'import opa_git_sync; print(opa_git_sync.__version__)')

all: test

.PHONY: build
build:
	docker build -t $(IMAGE) .

.PHONY: test
test: build test-unit test-flake8

.PHONY: test-unit
test-unit:
	docker run --rm $(IMAGE) py.test opa_git_sync

.PHONY: test-flake8
test-flake8:
	docker run --rm $(IMAGE) flake8

.PHONY: shell
shell: test
	docker run -it --rm $(IMAGE) bash

.PHONY: version
version:
	@echo $(VERSION)

.PHONY: tag
tag: build
	docker tag $(IMAGE) $(IMAGE):$(VERSION)

.PHONY: push
push: tag
	docker push $(IMAGE):$(VERSION)

.PHONY: release
release:
	./release.sh
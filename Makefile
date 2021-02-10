APP    := change
NAME   := ${APP}
TAG    := $$(git log -1 --pretty=%h) # eg 5d72e2b
SHA    := $$(git log -1 --pretty=%H) # eg 5d72e2b158be269390d4b3931ed5d0febd784fb5

IMAGE  := merkely/${APP}:master
IMAGE_BBPIPE := merkely/${APP}-bbpipe

LATEST := ${NAME}:latest
CONTAINER := ${NAME}

CDB_HOST=https://app.compliancedb.com
MERKELY_HOST=https://app.compliancedb.com

# all non-latest images - for prune target
IMAGES := $(shell docker image ls --format '{{.Repository}}:{{.Tag}}' $(NAME) | grep -v latest)

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

ifeq ($(CI),true)
	# no tty on CI
	DOCKER_RUN_TTY=
	DOCKER_RUN_INTERACTIVE=
else
	# colour on terminal needs tty
	DOCKER_RUN_TTY=--tty
	# pdb needs interactive
	DOCKER_RUN_INTERACTIVE=--interactive
endif


# list the targets: from https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile
.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs

# list installed Python packages and their version numbers
pip_list:
	@docker run --rm -it --entrypoint="" ${IMAGE} pip3 list

# - - - - - - - - - - - - - - - - - - - -
# full image rebuilds, with fresh base image, and no Docker caching

rebuild_all: rebuild rebuild_bb

rebuild: delete_base_image
	@docker build \
		--build-arg IMAGE_COMMIT_SHA=${SHA} \
		--file Dockerfile \
		--no-cache \
		--tag ${IMAGE} .
	@docker tag ${IMAGE} ${LATEST}

rebuild_bb: delete_base_image_bb
	@docker build \
		--build-arg IMAGE_COMMIT_SHA=${SHA} \
		--file Dockerfile.bb_pipe \
		--no-cache \
		--tag ${IMAGE_BBPIPE} .

delete_base_image: build
    # Get the ID of the image
	$(eval IMAGE_ID = $(shell docker image list --format "table {{.ID}} {{.Repository}}:{{.Tag}}" | grep "${IMAGE}" | awk '{print $$1}'))
	# Get the Dockerfile layers of the image
	$(eval IMAGE_LAYERS = $(shell docker run -v /var/run/docker.sock:/var/run/docker.sock --rm chenzj/dfimage ${IMAGE_ID}))
	# Get the base FROM image
	$(eval BASE_IMAGE = $(shell echo "${IMAGE_LAYERS}" | head -n 1 | awk '{print $$2}'))
	@docker image rm ${BASE_IMAGE}

delete_base_image_bb: build_bb
    # Get the ID of the image
	$(eval IMAGE_ID = $(shell docker image list --format "table {{.ID}} {{.Repository}}:{{.Tag}}" | grep "${IMAGE_BBPIPE}" | awk '{print $$1}'))
	# Get the Dockerfile layers of the image
	$(eval IMAGE_LAYERS = $(shell docker run -v /var/run/docker.sock:/var/run/docker.sock --rm chenzj/dfimage ${IMAGE_ID}))
	# Get the base FROM image
	$(eval BASE_IMAGE = $(shell echo "${IMAGE_LAYERS}" | head -n 1 | awk '{print $$2}'))
	@docker image rm ${BASE_IMAGE}

# - - - - - - - - - - - - - - - - - - - -
# image builds with Docker caching

build_all: build build_bb

build:
	@echo ${IMAGE}
	@docker build \
		--build-arg IMAGE_COMMIT_SHA=${SHA} \
		--file Dockerfile \
		--tag ${IMAGE} .
	@docker tag ${IMAGE} ${LATEST}

build_bb:
	@echo ${IMAGE_BBPIPE}
	@docker build \
		--build-arg IMAGE_COMMIT_SHA=${SHA} \
		--file Dockerfile.bb_pipe \
		--tag ${IMAGE_BBPIPE} .

# - - - - - - - - - - - - - - - - - - - -
# run tests without building by volume-mounting

test_all: test_unit test_integration test_bb_integration

define SOURCE_VOLUME_MOUNTS
	--volume ${ROOT_DIR}/cdb:/app/cdb \
	--volume ${ROOT_DIR}/commands:/app/commands \
	--volume ${ROOT_DIR}/env_vars:/app/env_vars \
	--volume ${ROOT_DIR}/fingerprinters:/app/fingerprinters
endef

define TESTS_VOLUME_MOUNT
    --volume ${ROOT_DIR}/tests:/app/tests
endef

test_unit:
	docker rm --force ${CONTAINER} 2> /dev/null || true
	$(eval COVERAGE_DIR = tmp/coverage/unit)
	rm -rf ${COVERAGE_DIR} && mkdir -p ${COVERAGE_DIR}
	docker run \
		--name ${CONTAINER} \
		${DOCKER_RUN_TTY} \
		${DOCKER_RUN_INTERACTIVE} \
		${SOURCE_VOLUME_MOUNTS} \
		${TESTS_VOLUME_MOUNT} \
	    --volume ${ROOT_DIR}/${COVERAGE_DIR}/htmlcov:/app/htmlcov \
		--entrypoint ./tests/unit/coverage_entrypoint.sh \
			${IMAGE} tests/unit/${TARGET}

test_integration:
	@docker rm --force ${CONTAINER} 2> /dev/null || true
	$(eval COVERAGE_DIR = tmp/coverage/integration)
	@rm -rf ${COVERAGE_DIR} && mkdir -p ${COVERAGE_DIR}
	@docker run \
		--name ${CONTAINER} \
		${DOCKER_RUN_TTY} \
		${DOCKER_RUN_INTERACTIVE} \
		${SOURCE_VOLUME_MOUNTS} \
		${TESTS_VOLUME_MOUNT} \
		--volume ${ROOT_DIR}/${COVERAGE_DIR}/htmlcov:/app/htmlcov \
		--entrypoint ./tests/integration/coverage_entrypoint.sh \
			${IMAGE} tests/integration/${TARGET}

test_bb_integration:
	@docker rm --force ${CONTAINER} 2> /dev/null || true
	$(eval COVERAGE_DIR = tmp/coverage/bb_integration)
	@rm -rf ${COVERAGE_DIR} && mkdir -p ${COVERAGE_DIR}
	@docker run \
		--name ${CONTAINER} \
		${DOCKER_RUN_TTY} \
		${DOCKER_RUN_INTERACTIVE} \
		${SOURCE_VOLUME_MOUNTS} \
		--volume ${ROOT_DIR}/bitbucket_pipe/pipe.py:/app/pipe.py \
		${TESTS_VOLUME_MOUNT} \
		--volume ${ROOT_DIR}/${COVERAGE_DIR}/htmlcov:/app/htmlcov \
		--entrypoint ./tests/bb_integration/coverage_entrypoint.sh \
			${IMAGE_BBPIPE} tests/bb_integration/${TARGET}

pytest_help:
	@docker run \
		--entrypoint="" \
		--rm \
		${IMAGE} \
		  python3 -m pytest --help

# - - - - - - - - - - - - - - - - - - - -

living_docs:
	@docker run \
        --rm \
        --volume ${ROOT_DIR}/scripts:/app/scripts \
        ${SOURCE_VOLUME_MOUNTS} \
        ${IMAGE} python /app/scripts/living_docs.py

DOCS_IMAGE := merkely/docs
build_docs_dockerfile:
	docker build -t ${DOCS_IMAGE} docs.merkely.com/

build_docs:
	@docker run --rm -v ${PWD}/docs.merkely.com:/docs -v ${PWD}/server/static:/global-assets ${DOCS_IMAGE} make html
	@cp -RP docs.merkely.com/build/html/. docs/.
# - - - - - - - - - - - - - - - - - - - -

push:
	@docker push ${IMAGE}

pull:
	@docker pull ${IMAGE}

# Enter running container with a shell
enter:
	@docker exec -ti ${CONTAINER} sh

# Follow the container logs
follow:
	@docker container logs -f ${CONTAINER}

# Start a container with shell
shell:
	@docker run -it --rm --name ${CONTAINER} ${IMAGE} sh

# Delete all the non-latest images
prune:
	@docker image rm $(IMAGES)

# Get the repo statistics
stats:
	@echo Commits: $$(git rev-list --count master)
	@cloc .

# - - - - - - - - - - - - - - - - - - - -
# recording tasks

MASTER_BRANCH := master
BRANCH_NAME := $(shell git rev-parse --abbrev-ref HEAD)
# Check if branch ends with master
ifeq ($(shell git rev-parse --abbrev-ref HEAD),master)
	IS_MASTER=TRUE
	PROJFILE=project-master.json
	MERKELYPIPE=project-master.json
else
	IS_MASTER=FALSE
	PROJFILE=project-pull-requests.json
	MERKELYPIPE=project-pull-requests.json
endif


branch:
	@echo Branch is ${BRANCH_NAME}
	@echo IS_MASTER is ${IS_MASTER}
	@echo PROJFILE is ${PROJFILE}

# - - - - - - - - - - - - - - - - - - - -
# Merkely commands

merkely_declare_pipeline:
	docker run \
			--env MERKELY_COMMAND=declare_pipeline \
			\
			--env MERKELY_API_TOKEN=${MERKELY_API_TOKEN} \
			--env MERKELY_HOST=${MERKELY_HOST} \
			--rm \
			--volume ${PWD}/${MERKELYPIPE}:/Merkelypipe.json \
			${IMAGE}

merkely_log_artifact:
	docker run \
			--env MERKELY_COMMAND=log_artifact \
			\
			--env MERKELY_FINGERPRINT="docker://${MERKELY_DOCKER_IMAGE}" \
			--env MERKELY_ARTIFACT_GIT_URL=${MERKELY_ARTIFACT_GIT_URL} \
			--env MERKELY_ARTIFACT_GIT_COMMIT=${MERKELY_ARTIFACT_GIT_COMMIT} \
			--env MERKELY_CI_BUILD_URL=${MERKELY_CI_BUILD_URL} \
			--env MERKELY_CI_BUILD_NUMBER=${MERKELY_CI_BUILD_NUMBER} \
			--env MERKELY_IS_COMPLIANT=${MERKELY_IS_COMPLIANT} \
			\
			--env MERKELY_API_TOKEN=${MERKELY_API_TOKEN} \
			--env MERKELY_HOST=${MERKELY_HOST} \
			--rm \
			--volume=/var/run/docker.sock:/var/run/docker.sock \
			--volume ${PWD}/${MERKELYPIPE}:/Merkelypipe.json \
			${IMAGE}

# - - - - - - - - - - - - - - - - - - - -
# CDB Commands

put_project:
	docker run \
			--env CDB_HOST=${CDB_HOST} \
			--env CDB_API_TOKEN=${CDB_API_TOKEN} \
			--rm \
			--volume ${PWD}/${PROJFILE}:/data/project.json \
			${IMAGE} python -m cdb.put_project -p /data/project.json

put_artifact_image:
	docker run \
			--env CDB_HOST=${CDB_HOST} \
			--env CDB_API_TOKEN=${CDB_API_TOKEN} \
			--env CDB_IS_COMPLIANT=${CDB_IS_COMPLIANT} \
			--env CDB_ARTIFACT_GIT_URL=${CDB_ARTIFACT_GIT_URL} \
			--env CDB_ARTIFACT_GIT_COMMIT=${CDB_ARTIFACT_GIT_COMMIT} \
			--env CDB_CI_BUILD_URL=${CDB_CI_BUILD_URL} \
			--env CDB_BUILD_NUMBER=${CDB_BUILD_NUMBER} \
			--env CDB_ARTIFACT_DOCKER_IMAGE=${CDB_ARTIFACT_DOCKER_IMAGE} \
			--rm \
			--volume=/var/run/docker.sock:/var/run/docker.sock \
 			--volume ${PWD}/${PROJFILE}:/data/project.json \
	        ${IMAGE} python -m cdb.put_artifact_image -p /data/project.json

publish_test_results:
	docker run \
			--env CDB_HOST=https://app.compliancedb.com \
			--env CDB_API_TOKEN=${CDB_API_TOKEN} \
			--env CDB_IS_COMPLIANT=${CDB_IS_COMPLIANT} \
			--env CDB_EVIDENCE_TYPE=${CDB_EVIDENCE_TYPE} \
			--env CDB_DESCRIPTION="${CDB_DESCRIPTION}" \
			--env CDB_BUILD_NUMBER=${CDB_BUILD_NUMBER} \
			--env CDB_CI_BUILD_URL=${CDB_CI_BUILD_URL} \
			--env CDB_ARTIFACT_DOCKER_IMAGE=${CDB_ARTIFACT_DOCKER_IMAGE} \
			--rm \
			--volume=/var/run/docker.sock:/var/run/docker.sock \
			--volume ${PWD}/${PROJFILE}:/data/project.json \
			${IMAGE} python -m cdb.put_evidence -p /data/project.json

control_and_publish_junit_results:
	docker run \
			--env CDB_HOST=https://app.compliancedb.com \
			--env CDB_API_TOKEN=${CDB_API_TOKEN} \
			--env CDB_EVIDENCE_TYPE=${CDB_EVIDENCE_TYPE} \
			--env CDB_CI_BUILD_URL=${CDB_CI_BUILD_URL} \
			--env CDB_ARTIFACT_DOCKER_IMAGE=${CDB_ARTIFACT_DOCKER_IMAGE} \
			--rm \
			--volume ${CDB_TEST_RESULTS}:/data/junit/junit.xml \
			--volume=/var/run/docker.sock:/var/run/docker.sock \
			--volume ${PWD}/${PROJFILE}:/data/project.json \
			${IMAGE} python -m cdb.control_junit -p /data/project.json

publish_evidence:
	docker run \
			--env CDB_HOST=${CDB_HOST} \
			--env CDB_API_TOKEN=${CDB_API_TOKEN} \
			--env CDB_IS_COMPLIANT=${CDB_IS_COMPLIANT} \
			--env CDB_EVIDENCE_TYPE=${CDB_EVIDENCE_TYPE} \
			--env CDB_DESCRIPTION="${CDB_DESCRIPTION}" \
			--env CDB_BUILD_NUMBER=${CDB_BUILD_NUMBER} \
			--env CDB_CI_BUILD_URL=${CDB_CI_BUILD_URL} \
			--rm \
			--env CDB_ARTIFACT_DOCKER_IMAGE=${CDB_ARTIFACT_DOCKER_IMAGE} \
			--volume=/var/run/docker.sock:/var/run/docker.sock \
			--volume ${PWD}/${PROJFILE}:/data/project.json \
			${IMAGE} python -m cdb.put_evidence -p /data/project.json

publish_release:
	IMAGE=${IMAGE} ./server/cdb/release.sh

create_release:
	# Always release from project-master.json project
	docker run \
			--env CDB_HOST=${CDB_HOST} \
			--env CDB_API_TOKEN=${CDB_API_TOKEN} \
			--env CDB_ARTIFACT_DOCKER_IMAGE=${CDB_ARTIFACT_DOCKER_IMAGE} \
			--env CDB_TARGET_SRC_COMMITISH=${CDB_TARGET_SRC_COMMITISH} \
			--env CDB_BASE_SRC_COMMITISH=${CDB_BASE_SRC_COMMITISH} \
			--env CDB_RELEASE_DESCRIPTION="${CDB_RELEASE_DESCRIPTION}" \
			--rm \
			--volume=/var/run/docker.sock:/var/run/docker.sock \
			--volume ${PWD}/project-master.json:/data/project.json \
			--volume ${PWD}:/src \
			${IMAGE} python -m cdb.create_release -p /data/project.json

control_latest_release:
	# Always release from project-master.json project
	docker run \
			--env CDB_HOST=${CDB_HOST} \
			--env CDB_API_TOKEN=${CDB_API_TOKEN} \
			--env CDB_ARTIFACT_SHA=${CDB_ARTIFACT_SHA} \
			--rm \
			--volume ${PWD}/project-master.json:/data/project.json \
			${IMAGE} python -m cdb.control_latest_release -p /data/project.json

create_deployment:
	docker run \
			--env CDB_HOST=${CDB_HOST} \
			--env CDB_API_TOKEN=${CDB_API_TOKEN} \
			--env CDB_ARTIFACT_DOCKER_IMAGE=${CDB_ARTIFACT_DOCKER_IMAGE} \
			--env CDB_ENVIRONMENT=test \
			--env CDB_CI_BUILD_URL=${CDB_CI_BUILD_URL} \
			--env CDB_DESCRIPTION="${CDB_DESCRIPTION}" \
			--rm \
			--volume ${PWD}:/src \
			--volume=/var/run/docker.sock:/var/run/docker.sock \
			--volume ${PWD}/project-master.json:/data/project.json \
			${IMAGE} python -m cdb.create_deployment -p /data/project.json

## Test dry runs
dry_run_put_artifact:
	docker run \
			--env CDB_HOST=${CDB_HOST} \
			--env CDB_API_TOKEN="${CDB_API_TOKEN}" \
			--env CDB_IS_COMPLIANT="TRUE" \
			--env CDB_ARTIFACT_GIT_URL="http://github/me/project/commits/3451345234523453245" \
			--env CDB_ARTIFACT_GIT_COMMIT="134125123541234123513425" \
			--env CDB_CI_BUILD_URL="https://gitlab/build/1234" \
			--env CDB_BUILD_NUMBER="1234" \
			--env CDB_ARTIFACT_FILENAME=/data/artifact.txt \
			--env CDB_DRY_RUN="TRUE" \
			--rm \
			--volume=/var/run/docker.sock:/var/run/docker.sock \
			--volume=${PWD}/Dockerfile:/data/artifact.txt \
 			--volume ${PWD}/${PROJFILE}:/data/project.json \
	        ${IMAGE} python -m cdb.put_artifact -p /data/project.json

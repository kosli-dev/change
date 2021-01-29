APP    := cdb_controls
NAME   := ${APP}
TAG    := $$(git log -1 --pretty=%h) # eg 5d72e2b
SHA    := $$(git log -1 --pretty=%H) # eg 5d72e2b158be269390d4b3931ed5d0febd784fb5

IMAGE  := compliancedb/${APP}
IMAGE_PIPE := compliancedb/${APP}-bbpipe

LATEST := ${NAME}:latest
CONTAINER := cdb_controls
REPOSITORY   := registry.gitlab.com/compliancedb/compliancedb/${APP}
SERVER_PORT := 8001

CDB_HOST=https://app.compliancedb.com

# all non-latest images - for prune target
IMAGES := $(shell docker image ls --format '{{.Repository}}:{{.Tag}}' $(NAME) | grep -v latest)

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

# list the targets: from https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile
.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs


build:
	@echo ${IMAGE}
	@docker build \
		--build-arg IMAGE_COMMIT_SHA=${SHA} \
		--file Dockerfile \
		--tag ${IMAGE} .
	@docker tag ${IMAGE} ${LATEST}


build_bb:
	@echo ${IMAGE_PIPE}
	@docker build \
		--build-arg IMAGE_COMMIT_SHA=${SHA} \
		--file Dockerfile.bb_pipe \
		--tag ${IMAGE_PIPE} .

test_all: test_unit test_integration test_bb_integration
test_all_build: test_unit_build test_integration_build test_bb_integration_build
test_unit_build: build test_unit
test_integration_build: build test_integration
test_bb_integration_build: build_bb test_bb_integration

test_unit:
	@docker rm --force 2> /dev/null $@ || true
	@rm -rf tmp/coverage/unit && mkdir -p tmp/coverage/unit
	@docker run \
		--name $@ \
		--tty `# for colour on terminal` \
		--volume ${ROOT_DIR}/cdb:/app/cdb \
		--volume ${ROOT_DIR}/tests:/app/tests \
		--volume ${ROOT_DIR}/tmp/coverage/unit/htmlcov:/app/htmlcov \
		--entrypoint ./tests/unit/coverage_entrypoint.sh \
			${IMAGE} tests/unit/${TARGET}

test_integration:
	@docker rm --force $@ 2> /dev/null || true
	@rm -rf tmp/coverage/integration && mkdir -p tmp/coverage/integration
	@docker run \
		--name $@ \
		--tty `# for colour on terminal` \
		--volume ${ROOT_DIR}/cdb:/app/cdb \
		--volume ${ROOT_DIR}/tests:/app/tests \
		--volume ${ROOT_DIR}/tmp/coverage/integration/htmlcov:/app/htmlcov \
		--entrypoint ./tests/integration/coverage_entrypoint.sh \
			${IMAGE} tests/integration/${TARGET}

test_bb_integration:
	@docker rm --force $@ 2> /dev/null || true
	@rm -rf tmp/coverage/bb_integration && mkdir -p tmp/coverage/bb_integration
	@docker run \
		--name $@ \
		--tty `# for colour on terminal` \
		--volume ${ROOT_DIR}/cdb:/app/cdb \
		--volume ${ROOT_DIR}/bitbucket_pipe/pipe.py:/app/pipe.py \
		--volume ${ROOT_DIR}/tests:/app/tests \
		--volume ${ROOT_DIR}/tmp/coverage/bb_integration/htmlcov:/app/htmlcov \
		--entrypoint ./tests/bb_integration/coverage_entrypoint.sh \
			${IMAGE_PIPE} tests/bb_integration/${TARGET}

pytest_help:
	@docker run \
		--entrypoint="" \
		--rm \
		${IMAGE} \
		  python3 -m pytest --help

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
	@docker run -it --rm -p ${SERVER_PORT}:${SERVER_PORT} --name ${CONTAINER} ${IMAGE} sh

# Delete all the non-latest images
prune:
	@docker image rm $(IMAGES)

# Get the repo statistics
stats:
	@echo Commits: $$(git rev-list --count master)
	@cloc .


# ComplianceDB recording tasks

MASTER_BRANCH := master
BRANCH_NAME := $(shell git rev-parse --abbrev-ref HEAD)
# Check if branch ends with master
ifeq ($(shell git rev-parse --abbrev-ref HEAD),master)
	IS_MASTER=TRUE
	PROJFILE=project-master.json
else
	IS_MASTER=FALSE
	PROJFILE=project-pull-requests.json
endif


branch:
	@echo Branch is ${BRANCH_NAME}
	@echo IS_MASTER is ${IS_MASTER}
	@echo PROJFILE is ${PROJFILE}

put_project:
	docker run --rm \
			--volume ${PWD}/${PROJFILE}:/data/project.json \
			--env CDB_HOST=${CDB_HOST} \
			--env CDB_API_TOKEN=${CDB_API_TOKEN} \
			${IMAGE} python -m cdb.put_project -p /data/project.json

merkely_declare_pipeline:
	docker run --rm \
			--volume ${PWD}/${PROJFILE}:/Merkelypipe.json \
			--env MERKELY_COMMAND=declare_pipeline \
			--env MERKELY_API_TOKEN=${CDB_API_TOKEN} \
			${IMAGE}

put_artifact_image:
	docker run --rm \
 			--volume ${PWD}/${PROJFILE}:/data/project.json \
			--volume=/var/run/docker.sock:/var/run/docker.sock \
			--env CDB_HOST=${CDB_HOST} \
			--env CDB_API_TOKEN=${CDB_API_TOKEN} \
			--env CDB_IS_COMPLIANT=${CDB_IS_COMPLIANT} \
			--env CDB_ARTIFACT_GIT_URL=${CDB_ARTIFACT_GIT_URL} \
			--env CDB_ARTIFACT_GIT_COMMIT=${CDB_ARTIFACT_GIT_COMMIT} \
			--env CDB_CI_BUILD_URL=${CDB_CI_BUILD_URL} \
			--env CDB_BUILD_NUMBER=${CDB_BUILD_NUMBER} \
			--env CDB_ARTIFACT_DOCKER_IMAGE=${CDB_ARTIFACT_DOCKER_IMAGE} \
	        ${IMAGE} python -m cdb.put_artifact_image -p /data/project.json

publish_test_results:
	docker run --rm \
			--volume ${PWD}/${PROJFILE}:/data/project.json \
			--volume=/var/run/docker.sock:/var/run/docker.sock \
			--env CDB_HOST=https://app.compliancedb.com \
			--env CDB_API_TOKEN=${CDB_API_TOKEN} \
			--env CDB_IS_COMPLIANT=${CDB_IS_COMPLIANT} \
			--env CDB_EVIDENCE_TYPE=${CDB_EVIDENCE_TYPE} \
			--env CDB_DESCRIPTION="${CDB_DESCRIPTION}" \
			--env CDB_BUILD_NUMBER=${CDB_BUILD_NUMBER} \
			--env CDB_CI_BUILD_URL=${CDB_CI_BUILD_URL} \
			--env CDB_ARTIFACT_DOCKER_IMAGE=${CDB_ARTIFACT_DOCKER_IMAGE} \
			${IMAGE} python -m cdb.put_evidence -p /data/project.json


control_and_publish_junit_results:
	docker run --rm \
			--volume ${PWD}/${PROJFILE}:/data/project.json \
			--volume ${CDB_TEST_RESULTS}:/data/junit/junit.xml \
			--volume=/var/run/docker.sock:/var/run/docker.sock \
			--env CDB_HOST=https://app.compliancedb.com \
			--env CDB_API_TOKEN=${CDB_API_TOKEN} \
			--env CDB_EVIDENCE_TYPE=${CDB_EVIDENCE_TYPE} \
			--env CDB_CI_BUILD_URL=${CDB_CI_BUILD_URL} \
			--env CDB_ARTIFACT_DOCKER_IMAGE=${CDB_ARTIFACT_DOCKER_IMAGE} \
			${IMAGE} python -m cdb.control_junit -p /data/project.json


publish_evidence:
	docker run --rm \
			--volume ${PWD}/${PROJFILE}:/data/project.json \
			--volume=/var/run/docker.sock:/var/run/docker.sock \
			--env CDB_HOST=${CDB_HOST} \
			--env CDB_API_TOKEN=${CDB_API_TOKEN} \
			--env CDB_IS_COMPLIANT=${CDB_IS_COMPLIANT} \
			--env CDB_EVIDENCE_TYPE=${CDB_EVIDENCE_TYPE} \
			--env CDB_DESCRIPTION="${CDB_DESCRIPTION}" \
			--env CDB_BUILD_NUMBER=${CDB_BUILD_NUMBER} \
			--env CDB_CI_BUILD_URL=${CDB_CI_BUILD_URL} \
			--env CDB_ARTIFACT_DOCKER_IMAGE=${CDB_ARTIFACT_DOCKER_IMAGE} \
			${IMAGE} python -m cdb.put_evidence -p /data/project.json

publish_release:
	IMAGE=${IMAGE} ./server/cdb/release.sh


create_release:
	# Always release from project-master.json project
	docker run --rm \
			--volume ${PWD}/project-master.json:/data/project.json \
			--volume ${PWD}:/src \
			--volume=/var/run/docker.sock:/var/run/docker.sock \
			--env CDB_HOST=${CDB_HOST} \
			--env CDB_API_TOKEN=${CDB_API_TOKEN} \
			--env CDB_ARTIFACT_DOCKER_IMAGE=${CDB_ARTIFACT_DOCKER_IMAGE} \
			--env CDB_TARGET_SRC_COMMITISH=${CDB_TARGET_SRC_COMMITISH} \
			--env CDB_BASE_SRC_COMMITISH=${CDB_BASE_SRC_COMMITISH} \
			--env CDB_RELEASE_DESCRIPTION="${CDB_RELEASE_DESCRIPTION}" \
			${IMAGE} python -m cdb.create_release -p /data/project.json


control_latest_release:
	# Always release from project-master.json project
	docker run --rm \
			--volume ${PWD}/project-master.json:/data/project.json \
			--env CDB_HOST=${CDB_HOST} \
			--env CDB_API_TOKEN=${CDB_API_TOKEN} \
			--env CDB_ARTIFACT_SHA=${CDB_ARTIFACT_SHA} \
			${IMAGE} python -m cdb.control_latest_release -p /data/project.json


create_deployment:
	docker run --rm \
			--volume ${PWD}/project-master.json:/data/project.json \
			--volume ${PWD}:/src \
			--volume=/var/run/docker.sock:/var/run/docker.sock \
			--env CDB_HOST=${CDB_HOST} \
			--env CDB_API_TOKEN=${CDB_API_TOKEN} \
			--env CDB_ARTIFACT_DOCKER_IMAGE=${CDB_ARTIFACT_DOCKER_IMAGE} \
			--env CDB_ENVIRONMENT=test \
			--env CDB_CI_BUILD_URL=${CDB_CI_BUILD_URL} \
			--env CDB_DESCRIPTION="${CDB_DESCRIPTION}" \
			${IMAGE} python -m cdb.create_deployment -p /data/project.json


## Test dry runs
dry_run_put_artifact:
	docker run --rm \
 			--volume ${PWD}/${PROJFILE}:/data/project.json \
			--volume=/var/run/docker.sock:/var/run/docker.sock \
			--volume=${PWD}/Dockerfile:/data/artifact.txt \
			--env CDB_HOST=${CDB_HOST} \
			--env CDB_API_TOKEN="${CDB_API_TOKEN}" \
			--env CDB_IS_COMPLIANT="TRUE" \
			--env CDB_ARTIFACT_GIT_URL="http://github/me/project/commits/3451345234523453245" \
			--env CDB_ARTIFACT_GIT_COMMIT="134125123541234123513425" \
			--env CDB_CI_BUILD_URL="https://gitlab/build/1234" \
			--env CDB_BUILD_NUMBER="1234" \
			--env CDB_ARTIFACT_FILENAME=/data/artifact.txt \
			--env CDB_DRY_RUN="TRUE" \
	        ${IMAGE} python -m cdb.put_artifact -p /data/project.json

copy_approvals:
	@docker logs test_integration | grep mv | sed 's/mv -f /docker cp test_integration:/' | sed 's/ \/app\// /'
	@docker logs test_unit        | grep mv | sed 's/mv -f /docker cp test_unit:/'        | sed 's/ \/app\// /'
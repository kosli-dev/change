APP    := cdb_controls
NAME   := ${APP}
TAG    := $$(git log -1 --pretty=%h)

IMAGE  := compliancedb/${APP}
IMAGE_PIPE := compliancedb/${APP}-bbpipe

LATEST := ${NAME}:latest
CONTAINER := cdb_controls
REPOSITORY   := registry.gitlab.com/compliancedb/compliancedb/${APP}
SERVER_PORT := 8001

CDB_HOST=https://app.compliancedb.com

# all non-latest images - for prune target
IMAGES := $(shell docker image ls --format '{{.Repository}}:{{.Tag}}' $(NAME) | grep -v latest)

# list the targets: from https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile
.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs


build:
	@echo ${IMAGE}
	@docker build -f Dockerfile -t ${IMAGE} .
	@docker tag ${IMAGE} ${LATEST}


build_pipe:
	@echo ${IMAGE_PIPE}
	@docker build -f Dockerfile.bb_pipe -t ${IMAGE_PIPE} .

# Github does not support volume mounts so we need to copy the test output from the container
# and capture the test exit value
test_unit: build
	@docker stop $@ || true
	@docker rm $@ || true
	@rm -rf tmp/coverage/unit
	@mkdir -p tmp/coverage/unit
	@docker run \
		--name $@ \
		--tty `# for colour on terminal` \
		--entrypoint ./unit_coverage_entrypoint.sh \
		${IMAGE} \
		tests/${TARGET} ; \
	e=$$?; \
	docker cp $@:/app/htmlcov/ tmp/coverage/unit; \
	exit $$e

test_unit_via_volume_mounts:
	@docker stop $@ || true
	@docker rm $@ || true
	@rm -rf tmp/coverage/unit
	@mkdir -p tmp/coverage/unit
	@docker run \
		--name $@ \
		--interactive `# eg pdb` \
		--tty `# for colour on terminal` \
		--volume ${PWD}/cdb:/app/cdb \
		--volume ${PWD}/integration_tests:/app/integration_tests \
		--volume ${PWD}/tests:/app/tests \
		--volume ${PWD}/tests_data:/app/tests_data \
		--entrypoint ./unit_coverage_entrypoint.sh \
		${IMAGE} \
		tests/${TARGET} \
	e=$$?; \
	docker cp $@:/app/htmlcov/ tmp/coverage/unit; \
	exit $$e

test_integration: build
	@docker stop $@ || true
	@docker rm $@ || true
	@rm -rf tmp/coverage/integration
	@mkdir -p tmp/coverage/integration
	@docker run \
		--name $@ \
		--tty `# for colour on terminal` \
		--entrypoint ./integration_coverage_entrypoint.sh \
		${IMAGE} \
		integration_tests/${TARGET} ; \
	e=$$?; \
	docker cp $@:/app/htmlcov/ tmp/coverage/integration; \
	exit $$e

test_integration_via_volume_mounts:
	@docker stop $@ || true
	@docker rm $@ || true
	@rm -rf tmp/coverage/integration
	@mkdir -p tmp/coverage/integration
	@docker run \
		--name $@ \
		--interactive `# eg pdb` \
		--tty `# for colour on terminal` \
		--volume ${PWD}/cdb:/app/cdb \
		--volume ${PWD}/integration_tests:/app/integration_tests \
		--volume ${PWD}/tests:/app/tests \
		--volume ${PWD}/tests_data:/app/tests_data \
		--entrypoint ./integration_coverage_entrypoint.sh \
		${IMAGE} \
		integration_tests/${TARGET} ; \
	e=$$?; \
	docker cp $@:/app/htmlcov/ tmp/coverage/integration; \
	exit $$e

test_all: test_unit test_integration

test_all_via_volume_mounts: test_unit_via_volume_mounts test_integration_via_volume_mounts

pytest_help:
	@docker run \
		--name pytest_help \
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
	docker run --rm --name comply \
			--volume ${PWD}/${PROJFILE}:/data/project.json \
			--env CDB_HOST=${CDB_HOST} \
			--env CDB_API_TOKEN=${CDB_API_TOKEN} \
			${IMAGE} python -m cdb.put_project -p /data/project.json

put_artifact_image:
	docker run --rm --name comply \
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
	docker run --rm --name comply \
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
	docker run --rm --name comply \
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
	docker run --rm --name comply \
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
	docker run --rm --name comply \
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
	docker run --rm --name comply \
			--volume ${PWD}/project-master.json:/data/project.json \
			--env CDB_HOST=${CDB_HOST} \
			--env CDB_API_TOKEN=${CDB_API_TOKEN} \
			--env CDB_ARTIFACT_SHA=${CDB_ARTIFACT_SHA} \
			${IMAGE} python -m cdb.control_latest_release -p /data/project.json


create_deployment:
	docker run --rm --name comply \
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
	docker run --rm --name comply \
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
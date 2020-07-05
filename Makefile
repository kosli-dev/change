APP    := cdb_controls
NAME   := ${APP}
TAG    := $$(git log -1 --pretty=%h)

ifdef CDB_CI_BUILD
IMAGE := ${CI_APPLICATION_REPOSITORY}:${CI_APPLICATION_TAG}
else
IMAGE  := ${NAME}:${TAG}
endif

LATEST := ${NAME}:latest
CONTAINER := cdb_controls
REPOSITORY   := registry.gitlab.com/compliancedb/compliancedb/${APP}
SERVER_PORT := 8001

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

push:
	@docker push ${IMAGE}
	@docker push ${LATEST}

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
# Check if branch ends with master, i.e. match origin/master AND master
ifeq ($(patsubst %$(MASTER_BRANCH),,$(lastword $(BRANCH_NAME))),)
	IS_MASTER=TRUE
	# Master branch builds are compliant
	IS_COMPLIANT=TRUE
	PROJFILE=cdb/project-master.json
else
	IS_MASTER=FALSE
	IS_COMPLIANT=FALSE
	PROJFILE=cdb/project-pull-requests.json
endif

GIT_URL=${CI_PROJECT_URL}/-/commit/${CI_COMMIT_SHA}

branch:
	@echo Branch is ${BRANCH_NAME}
	@echo IS_MASTER is ${IS_MASTER}
	@echo PROJFILE is ${PROJFILE}

ensure_project:
	docker run --rm --name comply ${IMAGE} python -m cdb.ensure_project -p ${PROJFILE}

publish_artifact:
	docker run --rm --name comply --volume=/var/run/docker.sock:/var/run/docker.sock \
	        --env IS_COMPLIANT=${IS_COMPLIANT} \
	        --env GIT_URL=${GIT_URL} \
	        --env GIT_COMMIT=${CI_COMMIT_SHA} \
	        --env JOB_DISPLAY_URL=${CI_JOB_URL} \
	        --env BUILD_TAG=${CI_JOB_ID} \
	        --env DOCKER_IMAGE=${IMAGE} \
	        --env CDB_API_TOKEN=${CDB_API_TOKEN} \
	        ${IMAGE} python -m cdb.publish_artifact -p ${PROJFILE}

publish_evidence:
	docker run --rm --name comply --volume=/var/run/docker.sock:/var/run/docker.sock \
	        --env IS_COMPLIANT=${IS_COMPLIANT} \
			--env EVIDENCE_TYPE=${CDB_EVIDENCE_TYPE} \
	        --env CDB_DESCRIPTION="${CDB_DESCRIPTION}" \
	        --env BUILD_TAG=${CI_JOB_ID} \
	        --env URL=${CI_JOB_URL} \
	        --env DOCKER_IMAGE=${IMAGE} \
			--env CDB_API_TOKEN=${CDB_API_TOKEN} \
	        ${IMAGE} python -m cdb.publish_evidence -p ${PROJFILE}

publish_release:
	IMAGE=${IMAGE} ./server/cdb/release.sh



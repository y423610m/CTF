export CTF_DOCKER_IMAGE_NAME=ctf_image
export CTF_DOCKER_CONTAINER_NAME=ctf_container

function ctf_build_docker(){
    docker build -t ${CTF_DOCKER_IMAGE_NAME} ${MY_CTF_DOCKER_ROOT}
}

function ctf_run_docker(){
    docker run  -v ~/CTF:/root/CTF --rm --name ${CTF_DOCKER_CONTAINER_NAME} -it ${CTF_DOCKER_IMAGE_NAME}
}

function ctf_exec_docker(){
    docker exec -it ${CTF_DOCKER_CONTAINER_NAME} bash
}

function ctf_commit_docker(){
    docker commit ${CTF_DOCKER_CONTAINER_NAME} ${CTF_DOCKER_IMAGE_NAME}:latest
}

function ctf_rm_docker(){
    containerid=$(docker ps | grep ${CTF_DOCKER_CONTAINER_NAME} | tail -n 1 | awk '{print $1}')
    docker kill ${containerid}
    containerid=$(docker ps -a | grep ${CTF_DOCKER_CONTAINER_NAME} | tail -n 1 | awk '{print $1}')
    docker rm ${containerid}
}

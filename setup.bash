MY_CTF_DOCKER_ROOT=$(pwd)
echo "#--- ctf docker scripts (${MY_CTF_DOCKER_ROOT}) ---" >> ~/.bashrc
echo "export MY_CTF_DOCKER_ROOT=${MY_CTF_DOCKER_ROOT}" >> ~/.bashrc 
echo "source ${MY_CTF_DOCKER_ROOT}/.bashrc" >> ~/.bashrc 

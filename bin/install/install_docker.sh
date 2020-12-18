#!/bin/bash

# install dependence soft of docker.
echo -e "\n\nInstall the dependence package of docker.\n\n"
sudo apt-get update && sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

if [ $? -ne 0 ]; then
    echo -e '\npre install of docker has failed.'
    exit 1
fi


# Add Docker’s official GPG key
echo -e "\n\nAdd Docker’s official GPG key.\n\n"
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -


# Verify Docker’s official GPG key.
echo -e "\n\nVerify Docker’s official GPG key.\n\n"
sudo apt-key fingerprint 0EBFCD88

# Add Docker’s official repository.
echo -e "\n\nAdd Docker’s official repository.\n\n"
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

if [ $? -ne 0 ]; then
    echo -e "\nadd repository of docker failed."
    exit 1
fi

echo -e "\n\nInstall stable version of docker '18.09.4~3-0~ubuntu-bionic' \n\n"
# sudo apt-get update && sudo apt-get install -y docker-ce=5:18.09.4~3-0~ubuntu-bionic docker-ce-cli=5:18.09.4~3-0~ubuntu-bionic containerd.io
sudo apt-get update && sudo apt-get install -y docker-ce docker-ce-cli containerd.io

sudo gpasswd -a ${USER} docker

sudo systemctl restart docker

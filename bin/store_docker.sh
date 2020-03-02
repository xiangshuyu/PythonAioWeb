#!/bin/bash

current_dir=`dirname $0`

all_images=$(docker images | awk 'NR>1{print $3}' | xargs)

if [ -d './docker_image' ];then
	echo -e "dir docker_image is exist.\n"
else
	echo -e "create dir docker_image to store images\n"
	mkdir -p $current_dir/docker_image
fi

for image in ${all_images}
do
	docker save $image -o $current_dir/docker_image/${image}.tar
done

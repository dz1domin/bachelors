#!/bin/bash

echo "Building image..."
imageHash=$(docker build .)
echo "Image has been built"
imageHash=$(echo "$imageHash" | grep -E -o 'Successfully built [0-9a-f]+' | cut -d' ' -f3)
echo "Running container..."
docker run "${imageHash}"
echo "Container finished his job"
echo "Copying result files to current directory..."
containerHash=$(docker ps -aqf "ancestor=${imageHash}" | head -qn 1)
echo "Copied"
echo "Removing container and image"
docker cp "${containerHash}:/root/ImageClassifier/bachelors-master" "result"
docker rm "$(docker ps -aqf "ancestor=${imageHash}")"
docker rmi "${imageHash}"

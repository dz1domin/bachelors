#!/bin/bash


clean=false
interactive=false

for option in "$@"
do
case $option in 
    -i|--interactive)
    interactive=true
    shift
    ;;
    -c|--clean)
    clean=true
    shift
    ;;
    *)
    
    ;;
esac
done


echo "Building image..."
imageHash=$(docker build .)
echo "Image has been built"
imageHash=$(echo "$imageHash" | grep -E -o 'Successfully built [0-9a-f]+' | cut -d' ' -f3)

echo "Running container..."
docker run "${imageHash}"
echo "Container finished his job"
echo "Copying result files to current directory..."
containerHash=$(docker ps -aqf "ancestor=${imageHash}" | head -qn 1)
docker cp "${containerHash}:/root/ImageClassifier/bachelors-master" "result"
echo "Copied"

if $interactive; then
    echo "Interactive mode"
    docker run -it --entrypoint /bin/bash "${imageHash}"
fi

if $clean; then
    echo "Removing container and image"
    docker rm -f "$(docker ps -aqf "ancestor=${imageHash}")"
    docker rmi -f "${imageHash}"
fi

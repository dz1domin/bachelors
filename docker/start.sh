#!/bin/bash

clean=false
interactive=false
quiet=false
user=false
WORKINGDIR=$(pwd)

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
    -q|--quiet)
    quiet=true
    shift
    ;;
    -u|--user)
    user=true
    shift
    ;;
    *)
    
    ;;
esac
done

REPODIR="bachelors"
echo "Checking repository directory..."
if [[ -d "$REPODIR" ]]; then
    echo "Repository already exists, pulling  to be up to date..."
    cd "${WORKINGDIR}/${REPODIR}" && git pull
    cd "$WORKINGDIR"
else
    echo "Repository does not exist, cloning..."
    git clone https://github.com/dz1domin/bachelors.git
fi

USERDIR="user_photos"
if [[ ! -d "$USERDIR" ]]; then
    mkdir "$USERDIR"
fi

cp "${WORKINGDIR}/${REPODIR}/docker/dockerfile" "${WORKINGDIR}"

echo "Building image..."
if $quiet; then
    imageHash=$(docker build .)
else
    imageHash=$(docker build . | tee /dev/tty )
fi

rm -f "${WORKINGDIR}/dockerfile" 2> /dev/null

echo "Image has been built."
imageHash=$(echo "$imageHash" | grep -E -o 'Successfully built [0-9a-f]+' | cut -d' ' -f3)

if $interactive; then
    echo "Interactive mode."
    docker run -it --entrypoint /bin/bash "${imageHash}"

elif $user; then
    echo "Running container with custom classifications..."
    docker run --entrypoint "/bin/bash" "$imageHash" "run_user_classifications.sh"
    echo "Finished."

else
    echo "Running container with default classifications..."
    docker run "${imageHash}"
    echo "Finished."
fi

rm -rf "${WORKINGDIR}/result" 2> /dev/null

echo "Copying result files to current directory..."
containerHash=$(docker ps -aqf "ancestor=${imageHash}" | head -qn 1)
docker cp "${containerHash}:/root/bachelors" "result"
echo "Copied."

if $clean; then
    echo "Removing container and image"
    docker rm -f "$(docker ps -aqf "ancestor=${imageHash}")"
    docker rmi -f "${imageHash}"
fi

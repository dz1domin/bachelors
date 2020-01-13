#!/bin/bash

classifier=$1
user=false
vis_name="default"

for option in "$@"
do
case $option in 
    -u|--user)
    user=true
    vis_name="user_photos"
    shift
    ;;
    cnn|fourier|laplace)
    classifier=$option
    shift
    ;;
    *)

    ;;
esac
done

echo "Running $classifier"
if $user; then
     CMD="/opt/conda/bin/python ImageClassificator.py \
        -p user_photos/ -r -a report ${classifier}"
else
    CMD="/opt/conda/bin/python ImageClassificator.py \
        -p PrepareSamples/ -r -v PrepareSamples/validation.json -z BlurValidator -a copy ${classifier}"
fi

if [ "$classifier" == "cnn" ]; then
    $CMD -visualization vis
    mv "vis" "${vis_name}_vis" 2>/dev/null
else
    $CMD
fi

if $user; then
    mv "Output" "${classifier}_user_dir_Output"
else
    mv "Output" "${classifier}_Output"
    mv "validation_result.json" "${classifier}_validation_result.json"
fi
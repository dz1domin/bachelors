#!/bin/bash

CLASSIFIER=$1
echo "Running $CLASSIFIER"
CMD="python ImageClassificator.py \
 -p PrepareSamples/ -r -v PrepareSamples/validation.json -z BlurValidator -a copy ${CLASSIFIER}"

if [ "$CLASSIFIER" == "cnn" ]; then
    $CMD -visualization vis
else
    $CMD
fi
mv "Output" "${CLASSIFIER}_Output"
mv "validation_result.json" "${CLASSIFIER}_validation_result.json"
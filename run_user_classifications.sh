#!/bin/bash

echo "Running classification for user input"
bash ./run_classification.sh "laplace" -u
bash ./run_classification.sh "fourier" -u
bash ./run_classification.sh "cnn" -u
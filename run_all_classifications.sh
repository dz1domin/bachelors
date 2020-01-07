#!/bin/bash


echo "Running all three classifiers with validation"
bash ./run_classification.sh "laplace"
bash ./run_classification.sh "fourier"
bash ./run_classification.sh "cnn"

echo "Running classification for user input"
bash ./run_classification.sh "laplace" -c
bash ./run_classification.sh "fourier" -c
bash ./run_classification.sh "cnn" -c
echo "DONE"
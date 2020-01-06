#!/bin/bash


echo "Running all three classifiers with validation"
bash ./run_classification.sh "laplace"
bash ./run_classification.sh "fourier"
bash ./run_classification.sh "cnn"
echo "DONE"
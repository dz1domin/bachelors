#! /bin/bash

cd include
ln -s ../../../src/include/ModelConfig.hpp
cd ../src
ln -s ../../../src/src/ModelConfig.cpp
cd ..

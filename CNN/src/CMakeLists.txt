cmake_minimum_required(VERSION 3.10)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

project (CNN)

#modify HINTS here
find_package(Torch REQUIRED HINTS /home/miloszek/libs/libtorch/libtorch)
find_package(OpenCV REQUIRED HINTS /home/miloszek/libs/opencv/opencv-4.1.2)
find_package(Boost COMPONENTS python3 system REQUIRED)
find_package(PythonLibs 3.7 REQUIRED)

include_directories(
    ${PROJECT_SOURCE_DIR}/include
    ${PROJECT_SOURCE_DIR}/src
)
include_directories(${PYTHON_INCLUDE_DIRS})

file(GLOB SOURCES
    "${PROJECT_SOURCE_DIR}/include/*.hpp"
    "${PROJECT_SOURCE_DIR}/src/*.cpp"
    )

add_library(cnn SHARED  ${SOURCES})
set_target_properties(cnn PROPERTIES SUFFIX ".so")
set_target_properties(cnn PROPERTIES PREFIX "")
target_link_libraries(cnn ${TORCH_LIBRARIES} ${OpenCV_LIBRARIES} ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})


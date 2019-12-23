cmake_minimum_required(VERSION 3.10)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(CMAKE_CXX_COMPILER g++-9)
set(CMAKE_C_COMPILER gcc-9)

project (CNN)

#modify HINTS here
find_package(Torch REQUIRED HINTS /home/miloszek/libs/libtorch/libtorch)
find_package(OpenCV REQUIRED HINTS /home/miloszek/libs/opencv/opencv-4.1.2)
find_package(Boost COMPONENTS python3 system REQUIRED)
find_package(PythonLibs 3.7 REQUIRED)
find_package(GTest REQUIRED)

include(GoogleTest)
include_directories(
    ${PROJECT_SOURCE_DIR}/include
    ${PROJECT_SOURCE_DIR}/src
)
include_directories(${PYTHON_INCLUDE_DIRS})

message("${GTest_LIBRARY}")

file(GLOB SOURCES
    "${PROJECT_SOURCE_DIR}/include/*.hpp"
    "${PROJECT_SOURCE_DIR}/src/*.cpp"
    )

add_executable(ModelConfig_UT ${SOURCES})

gtest_discover_tests(ModelConfig_UT)
target_link_libraries(ModelConfig_UT ${TORCH_LIBRARIES} ${OpenCV_LIBRARIES} ${Boost_LIBRARIES} ${PYTHON_LIBRARIES} ${GTEST_BOTH_LIBRARIES})

# add_custom_command(TARGET ModelConfig_UT
#                     PRE_BUILD
#                     COMMAND /bin/sh ./prepare_links.sh
#                     )

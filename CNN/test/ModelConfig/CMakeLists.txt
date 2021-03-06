cmake_minimum_required(VERSION 3.10)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(CMAKE_CXX_COMPILER g++-9)
set(CMAKE_C_COMPILER gcc-9)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -pedantic-errors")

project (CNN)

find_package(Torch REQUIRED)
find_package(OpenCV REQUIRED)
find_package(Boost COMPONENTS python3 system REQUIRED)
find_package(PythonLibs 3.7 REQUIRED)
find_package(GTest REQUIRED)

include(GoogleTest)
include_directories(
    ${PROJECT_SOURCE_DIR}/include
    ${PROJECT_SOURCE_DIR}/src
)
include_directories(${PYTHON_INCLUDE_DIRS})

file(GLOB SOURCES
    "${PROJECT_SOURCE_DIR}/include/*.hpp"
    "${PROJECT_SOURCE_DIR}/src/*.cpp"
    )

add_executable(ModelConfig_UT ${SOURCES})
target_link_libraries(ModelConfig_UT ${TORCH_LIBRARIES} ${OpenCV_LIBRARIES} ${Boost_LIBRARIES} ${PYTHON_LIBRARIES} ${GTEST_BOTH_LIBRARIES})

add_custom_target(run
            COMMAND ModelConfig_UT
            DEPENDS ModelConfig_UT
            WORKING_DIRECTORY ${CMAKE_PROJECT_DIR}
            )


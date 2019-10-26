#include "ImageProcessorFactory.hpp"
#include "ImageProcessorIdentifiers.hpp"
#include <iostream>

int main()
{
    ImageProcessorFactory factory;
    boost::property_tree::ptree tree;
    auto imageprocessor = factory.createImageProcessor(ANALYTICAL_ID, tree);
    std::cout << imageprocessor->getMyName() << std::endl;

}
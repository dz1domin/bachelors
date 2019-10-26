#include "MLImageProcessor.hpp"

MLImageProcessor::MLImageProcessor(boost::property_tree::ptree& inputTree) : ImageProcessor(inputTree)
{

}

void MLImageProcessor::doPreProcessing()
{

}

void MLImageProcessor::doProcessing()
{

}

void MLImageProcessor::doPostProcessing()
{


}

std::string MLImageProcessor::getMyName() const
{
    return "MLImageProcessor";
}
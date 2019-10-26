#include "AnalyticalImageProcessor.hpp"


AnalyticalImageProcessor::AnalyticalImageProcessor(boost::property_tree::ptree& inputTree) : ImageProcessor(inputTree)
{

}

void AnalyticalImageProcessor::doPreProcessing()
{

}

void AnalyticalImageProcessor::doProcessing()
{

}

void AnalyticalImageProcessor::doPostProcessing()
{


}

std::string AnalyticalImageProcessor::getMyName() const
{
    return "AnalyticalImageProcessor";
}
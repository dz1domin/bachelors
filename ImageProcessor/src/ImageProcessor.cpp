#include "ImageProcessor.hpp"


void ImageProcessor::process()
{
	doPreProcessing();
	doProcessing();
	doPostProcessing();
}

boost::property_tree::ptree ImageProcessor::getResults() const
{
	return m_output;
}

ImageProcessor::ImageProcessor(boost::property_tree::ptree& input_data) : m_input(input_data)
{

}

decltype(auto) ImageProcessor::_prepareJSON()
{
    return nullptr;
}

decltype(auto) ImageProcessor::_prepareResults()
{
    return nullptr;
}

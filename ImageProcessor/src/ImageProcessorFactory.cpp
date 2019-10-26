

#include "ImageProcessorFactory.hpp"
#include "ImageProcessorIdentifiers.hpp"
#include "AnalyticalImageProcessor.hpp"
#include "MLImageProcessor.hpp"
#include "DummyImageProcessor.hpp"

std::unique_ptr<ImageProcessor> ImageProcessorFactory::createImageProcessor(int methodID, boost::property_tree::ptree& ptreeInput)
{
    switch(methodID)
    {
        case ANALYTICAL_ID:
            return std::make_unique<AnalyticalImageProcessor>(ptreeInput);
            break;
        case ML_ID:
            return std::make_unique<MLImageProcessor>(ptreeInput);
            break;
        default:
            break;
    }
    return std::make_unique<DummyImageProcessor>();
}

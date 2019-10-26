/** File name: AnalyticalImageProcessor.hpp
 *  Author(s): Milosz Filus
 * 
 * History of changes
 * 
 * Version      Author      Change
 * v1           Milosz      Initial
 * ***********************************
**/

#ifndef __ANALYTICAL_IMAGE_PROCESSOR_HPP__
#define __ANALYTICAL_IMAGE_PROCESSOR_HPP__

#include "ImageProcessor.hpp"

class AnalyticalImageProcessor : public ImageProcessor
{
public:
    AnalyticalImageProcessor(boost::property_tree::ptree& inputTree);
    virtual void doPreProcessing();
    virtual void doProcessing();
    virtual void doPostProcessing();
    virtual std::string getMyName() const;
};

#endif

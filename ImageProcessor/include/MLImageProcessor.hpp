/** File name: MLImageProcessor.hpp
 *  Author(s): Milosz Filus
 * 
 * History of changes
 * 
 * Version      Author      Change
 * v1           Milosz      Initial
 * ***********************************
**/

#ifndef __ML_IMAGE_PROCESSOR_HPP__
#define __ML_IMAGE_PROCESSOR_HPP__

#include "ImageProcessor.hpp"

class MLImageProcessor : public ImageProcessor
{
public:
    MLImageProcessor(boost::property_tree::ptree& inputTree);
    virtual void doPreProcessing();
    virtual void doProcessing();
    virtual void doPostProcessing();
    virtual std::string getMyName() const;

};


#endif

/** File name: MLImageProcessor.hpp
 *  Author(s): Milosz Filus
 * 
 * History of changes
 * 
 * Version      Author      Change
 * v1           Milosz      Initial
 * ***********************************
**/

#ifndef __DUMMY_IMAGE_PROCESSOR_HPP__
#define __DUMMY_IMAGE_PROCESSOR_HPP__

#include "ImageProcessor.hpp"

class DummyImageProcessor : public ImageProcessor
{
public:
    virtual void doPreProcessing(){}
    virtual void doProcessing(){}
    virtual void doPostProcessing(){}
    virtual std::string getMyName() const { return "DummyImageProcessor"; }

};


#endif

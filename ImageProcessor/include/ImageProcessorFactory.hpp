/** File name: ImageProcessorFactory.hpp
 *  Author(s): Milosz Filus
 * 
 * History of changes
 * 
 * Version      Author      Change
 * v1           Milosz      Initial
 * ***********************************
**/

#ifndef __IMAGE_PROCESSOR_FACTORY_HPP__
#define __IMAGE_PROCESSOR_FACTORY_HPP__

#include <memory>
#include "ImageProcessor.hpp"

class ImageProcessorFactory
{
public:
    std::unique_ptr<ImageProcessor> createImageProcessor(int methodID, boost::property_tree::ptree& ptreeInput);
};








#endif

/** File name: ImageProcessor.hpp
 *  Author(s): Milosz Filus
 * 
 * History of changes
 * 
 * Version      Author      Change
 * v1           Milosz      Initial
 * ***********************************
**/

#ifndef __IMAGE_PROCESSOR_HPP__
#define __IMAGE_PROCESSOR_HPP__


#include <boost/property_tree/ptree.hpp>
#include <string>

class ImageProcessor
{
public:
    virtual void doPreProcessing() = 0;
    virtual void doProcessing() = 0;
    virtual void doPostProcessing() = 0;
    virtual std::string getMyName() const = 0;
	virtual void process();
	
	boost::property_tree::ptree getResults() const;

protected:
    ImageProcessor(boost::property_tree::ptree& input_data);
    ImageProcessor(){}
    decltype(auto) _prepareJSON();
    decltype(auto) _prepareResults();

private:
    boost::property_tree::ptree m_input;
    boost::property_tree::ptree m_output;
};


#endif

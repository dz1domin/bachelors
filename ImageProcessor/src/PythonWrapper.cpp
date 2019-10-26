#include <boost/python.hpp>
#include <any>
#include <iostream>
#include "ImageProcessorFactory.hpp"
#include "PythonWrapper.hpp"


#define DEBUG

const char* processImage(const char* json, int methodID)
{
	try 
	{
		std::cout << "Processing has been started. It may take a while..." << std::endl;
#ifdef DEBUG
		std::cout << "Input: " << json << " method: " << methodID << std::endl;
#endif
		boost::property_tree::ptree input(json);
		ImageProcessorFactory imageProcessorFactory;
		auto imageProcessor = imageProcessorFactory.createImageProcessor(methodID, input);
		imageProcessor->process();
		return imageProcessor->getResults().data().c_str();
	}
	catch (std::exception& e)
	{
		std::cerr << e.what() << std::endl;
	}
	
	return "Invalid input JSON";
}


BOOST_PYTHON_MODULE(ImageProcessor)
{
	boost::python::def("processImage", processImage, boost::python::args("input_json", "methodID"));
}

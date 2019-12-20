/** File name: PythonWrapper.cpp
 *  Author(s): Milosz Filus
 *
 * History of changes
 *
 * Version      Author      Change
 * v1           Milosz      Initial
 * ***********************************
**/




#include <boost/python.hpp>
#include <iostream>
#include "PythonWrapper.hpp"
#include "CNNBlurDetector.hpp"
#include <string>


boost::python::tuple cnn(boost::python::object& imagePath, boost::python::dict& optionDict)
{
	
	BlurDetector::ModelConfig config(boost::python::extract<std::string>(imagePath), optionDict);
	if (!config.isValid())
	{
		return boost::python::make_tuple(imagePath, std::string(BlurDetector::ResultTypes[BlurDetector::PROCESSING_ERROR]));
	}

	BlurDetector::CNNBlurDetector detector(config);
	auto result = detector.classify();


	if (config.shouldCreateDetailedImage())
	{
		detector.createImageWithCropsClassification(config.getVisualizationPath());
	}

	result = std::string(result == BlurDetector::ResultTypes[BlurDetector::BLURRED] ? "False" : "True");
	return boost::python::make_tuple(imagePath, result);
}


BOOST_PYTHON_MODULE(cnn)
{
	boost::python::def("cnn", cnn, boost::python::args("imagePath", "options"));
}

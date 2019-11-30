/** File name: ModelConfig.cpp
 *  Author(s): Milosz Filus
 *
 * History of changes
 *
 * Version      Author      Change
 * v1           Milosz      Initial
 * ***********************************
**/


#include "ModelConfig.hpp"
#include <exception>
#include <iostream>

#include <boost/python/extract.hpp>
#include <sstream>


BlurDetector::ModelConfig::ModelConfig(const std::string& imgPath, const boost::python::dict& input) noexcept
{
	try
	{
		m_imagePath = imgPath;

		if (!input.has_key("modelPath")) { return; }
		m_modelPath = boost::python::extract<std::string>(input.get("modelPath"));

		if (!input.has_key("thresh")) { return; }
		m_threshold = std::stod(boost::python::extract<std::string>(input.get("thresh")));

		if (!input.has_key("visualization")) { return; }
		
		m_shouldCreateDetailedImage = (std::string_view("true") == static_cast<std::string>(boost::python::extract<std::string>(input.get("visualization"))));

		if (m_shouldCreateDetailedImage)
		{
			if (!input.has_key("visualizationPath")) { return; }
			m_visualizationPath = boost::python::extract<std::string>(input.get("visualizationPath"));
		}

		m_isValid = true;
	}
	catch (std::exception& e)
	{
		std::cout << e.what() << std::endl;
	}

}

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
		if (auto val = boost::python::extract<std::string>(input.get("modelPath")); val.check())
		{ m_modelPath = val(); }
		else { return; };

		if (!input.has_key("thresh")) { return; }
		if (auto val = boost::python::extract<std::string>(input.get("thresh")); val.check())
		{ m_threshold = std::stod(val()); }
		else { return; }

		if (m_threshold < 0 || m_threshold > 1) { return; }


		if (!input.has_key("visualization")) { return; }
		if(auto val = boost::python::extract<std::string>(input.get("visualization")); val.check())
		{ m_shouldCreateDetailedImage = (std::string_view("true") == val()); }
		else { return; }

		if (m_shouldCreateDetailedImage)
		{
			if (!input.has_key("visualizationPath")) { return; }
			if(auto val = boost::python::extract<std::string>(input.get("visualizationPath")); val.check())
			{ m_visualizationPath = val(); }
			else { return; }
		}

		m_isValid = true;
	}
	catch (std::exception& e)
	{
		std::cout << e.what() << std::endl;
	}

}

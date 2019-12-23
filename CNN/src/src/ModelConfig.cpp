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

		auto res_1 = m_imagePath.rfind('/');
		auto res_2 = m_imagePath.rfind('\\');
		if (res_1 != std::string::npos && res_2 != std::string::npos)
		{
			auto max_res = res_1 > res_2 ? res_1 : res_2;
			m_imageName = std::string(m_imagePath, max_res + 1);
		}
		else if (res_1 != std::string::npos)
		{
			m_imageName = std::string(m_imagePath, res_1 + 1);
		}
		else if (res_2 != std::string::npos)
		{
			m_imageName = std::string(m_imagePath, res_2 + 1);
		}
		else
		{
			m_imageName = m_imagePath;
		}


		if (!input.has_key("modelPath")) { return; }
		if (auto val = boost::python::extract<std::string>(input.get("modelPath")); val.check())
		{ m_modelPath = val(); }
		else { return; };

		if (!input.has_key("thresh")) { return; }
		if (auto val = boost::python::extract<std::string>(input.get("thresh")); val.check())
		{ m_threshold = std::stod(val()); }
		else { return; }

		if (m_threshold < 0 || m_threshold > 1) { return; }


		if (input.has_key("visualization"))
		{
			if (auto val = boost::python::extract<std::string>(input.get("visualization")); val.check())
			{
				m_visualizationPath = val();
				m_shouldCreateDetailedImage = true;
			}
		}
		
		m_isValid = true;
	}
	catch (std::exception& e)
	{
		std::cout << e.what() << std::endl;
	}

}


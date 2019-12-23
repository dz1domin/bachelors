/** File name: ModelConfig.cpp
 *  Author(s): Milosz Filus
 *
 * History of changes
 *
 * Version      Author      Change
 * v1           Milosz      Initial
 * ***********************************
**/



#ifndef __MODEL_CONFIG_HPP__
#define __MODEL_CONFIG_HPP__


#include <string>
#include <boost/python/object.hpp>
#include <boost/python/tuple.hpp>
#include <boost/python/dict.hpp>

namespace BlurDetector
{

	class ModelConfig
	{
	public:
		explicit ModelConfig(const std::string& imgPath, const boost::python::dict& input) noexcept;
		
		bool isValid() const noexcept { return m_isValid; }
		double getThreshold() const noexcept { return m_threshold; }
		const std::string& getImagePath() const noexcept { return m_imagePath; }
		const std::string& getModelPath() const noexcept { return m_modelPath; }
		bool shouldCreateDetailedImage() const noexcept { return m_shouldCreateDetailedImage; }
		const std::string& getVisualizationPath() const noexcept { return m_visualizationPath; }
		const std::string& getImageName() const noexcept { return m_imageName; }



	private:

		double m_threshold = 0.0;
		std::string m_imagePath = "INVALID";
		std::string m_modelPath = "INVALID";
		std::string m_visualizationPath = "INVALID";
		std::string m_imageName = "INVALID";
		bool m_shouldCreateDetailedImage = false;
		bool m_isValid = false;


	};









}



#endif

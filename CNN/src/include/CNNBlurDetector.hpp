/** File name: CNNBlurDetector.hpp
 *  Author(s): Milosz Filus
 * 
 * History of changes
 * 
 * Version      Author      Change
 * v1           Milosz      Initial
 * ***********************************
**/

#ifndef __CNN_BLUR_DETECTOR_HPP__
#define __CNN_BLUR_DETECTOR_HPP__

#include <opencv2/opencv.hpp>
#include <exception>
#include <torch/jit.h>
#include "ModelConfig.hpp"
#include <utility>


namespace BlurDetector
{

	enum ResultIndex_t
	{
		SHARP,
		BLURRED,
		PROCESSING_ERROR,
		NUM_OF_RESULTS
	};

	constexpr std::array<const char*, NUM_OF_RESULTS> ResultTypes{ "SHARP", "BLURRED", "PROCESSING_ERROR" };
	constexpr unsigned int CROP_SIZE = 64;

	// Main processing class

	class CNNBlurDetector
	{
	public:
		explicit CNNBlurDetector(const ModelConfig& config) noexcept;

	public:

		std::string classify() noexcept;
		void createImageWithCropsClassification(std::string) const;



	private:

		void loadImage();
		void prepareImageAndCrops();
		void loadModel();
		void processImage();
		std::string getClassificationResult() const;

		void normalizeTensor(at::Tensor& tensor) const;

		cv::Mat initializeMask(unsigned int squareSize, unsigned int blue, unsigned int green, unsigned int red);


	private:
		static constexpr double NORMALIZATON_STDEV = 0.5;
		static constexpr double NORMALIZATON_MEAN = 0.5;
		static constexpr unsigned int PROCESSING_IMAGE_CHANNELS = 3;

	private:
		const ModelConfig m_config;

		std::vector< std::pair < cv::Rect, cv::Mat > > m_preparedCrops;
		std::vector < std::pair< cv::Rect, int > > m_cropsClassification;
		cv::Mat m_originalImage;
		torch::jit::script::Module m_trainedModel;



	private:
		// Exception class to inform user about processing errors

		class CNNBlurDetectorException : public std::exception
		{

		public:
			CNNBlurDetectorException(const char* message) : m_message(message) {}

		public:
			const char* what() const noexcept override
			{
				return m_message.c_str();
			}

		private:
			std::string m_message;

		};

	};


	


}




#endif

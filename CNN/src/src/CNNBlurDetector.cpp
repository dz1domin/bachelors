/** File name: CNNBlurDetector.cpp
 *  Author(s): Milosz Filus
 *
 * History of changes
 *
 * Version      Author      Change
 * v1           Milosz      Initial
 * ***********************************
**/




#include "CNNBlurDetector.hpp"

#include <torch/torch.h>
#include <torch/script.h>

using namespace BlurDetector;



CNNBlurDetector::CNNBlurDetector(const ModelConfig& config) noexcept : m_config(config)
{
	
}

std::string CNNBlurDetector::classify() noexcept
{
	try 
	{
		if (!m_config.isValid()){ throw CNNBlurDetectorException("Provided invalid config"); }

		loadImage();
		loadModel();
		prepareImageAndCrops();
		processImage();

		return getClassificationResult();
	}
	catch (std::exception& e)
	{
		std::cout << e.what() << std::endl;
	}
	return ResultTypes[PROCESSING_ERROR];
}

void CNNBlurDetector::loadImage()
{
	m_originalImage = cv::imread(m_config.getImagePath(), cv::IMREAD_UNCHANGED);
	if (m_originalImage.empty())
	{
		throw CNNBlurDetectorException("Cannot open image");
	}

	cv::resize(m_originalImage, m_originalImage, cv::Size(
		m_originalImage.cols - m_originalImage.cols % CROP_SIZE,
		m_originalImage.rows - m_originalImage.rows % CROP_SIZE));

}

void CNNBlurDetector::prepareImageAndCrops()
{
	for (int h = 0; h < m_originalImage.rows; h += CROP_SIZE)
	{
		for (int w = 0; w < m_originalImage.cols; w += CROP_SIZE)
		{
			m_preparedCrops.emplace_back(cv::Rect(w, h, CROP_SIZE, CROP_SIZE), 
				m_originalImage(cv::Rect( w, h, CROP_SIZE, CROP_SIZE )));


			auto&[rect, crop] = m_preparedCrops.back();
			cv::cvtColor(crop, crop, cv::COLOR_BGR2RGB);
			crop.convertTo(crop, CV_32FC3, 1.0 / 255.0);

		}
	}
}

void BlurDetector::CNNBlurDetector::loadModel()
{
	m_trainedModel = torch::jit::load(m_config.getModelPath());
}

void CNNBlurDetector::processImage()
{

	for (auto&[rect, crop] : m_preparedCrops)
	{
		// 1 in below function menas batch size 
		at::Tensor cropTensor = torch::from_blob(crop.data, { 1, CROP_SIZE, CROP_SIZE, PROCESSING_IMAGE_CHANNELS }, at::kFloat);
		cropTensor = cropTensor.permute({ 0, 3, 1, 2 });
		normalizeTensor(cropTensor);

		at::Tensor predictionResult = m_trainedModel.forward({ cropTensor }).toTensor();

		float sharpValue = predictionResult[0][SHARP].item<float>();
		float blurValue = predictionResult[0][BLURRED].item<float>();

		m_cropsClassification.emplace_back(rect, sharpValue > blurValue ? SHARP : BLURRED);

	}

}

void BlurDetector::CNNBlurDetector::normalizeTensor(at::Tensor & tensor) const
{
	for (unsigned int ch = 0; ch < PROCESSING_IMAGE_CHANNELS; ++ch)
	{
		tensor[0][ch] = tensor[0][ch].sub(NORMALIZATON_STDEV).div(NORMALIZATON_MEAN);
	}
}


void CNNBlurDetector::createImageWithCropsClassification(std::string pathToSave) const
{
	if (m_cropsClassification.empty())
	{
		std::cout << "Cannot create image with classified crops without running classify first" << std::endl;
		return;
	}

	static cv::Mat greenMask = cv::Mat(CROP_SIZE, CROP_SIZE, CV_8UC3, { 0, 255, 0 });
	static cv::Mat redMask = cv::Mat(CROP_SIZE, CROP_SIZE, CV_8UC3, { 0, 0, 255 });

	cv::Mat outputImg(m_originalImage.rows, m_originalImage.cols, CV_8UC3);
	for (auto&[rect, classificationResult] : m_cropsClassification)
	{
		cv::addWeighted(m_originalImage(rect), 1.0, (classificationResult == SHARP ? greenMask : redMask), 0.2, 0, outputImg(rect));
	}

	try 
	{
		cv::imwrite(pathToSave, outputImg);
	}
	catch (std::exception& e)
	{
		std::cout << e.what() << std::endl;
	}

}

std::string CNNBlurDetector::getClassificationResult() const
{
	int cropsNum = m_cropsClassification.size();
		
	int sharpCrops = std::count_if(m_cropsClassification.begin(), m_cropsClassification.end(),
		[=](const auto& elemPair) { return SHARP == elemPair.second;} );


	if (static_cast<double>(sharpCrops) / static_cast<double>(cropsNum) > m_config.getThreshold())
	{
		return ResultTypes[SHARP];
	}
	return ResultTypes[BLURRED];
}

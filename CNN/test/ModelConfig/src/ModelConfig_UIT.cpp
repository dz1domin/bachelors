#include "ModelConfig_UT.hpp"
#include <gtest/gtest.h>
#include "ModelConfig.hpp"
#include <memory>
#include <filesystem>
#include <vector>


class ModelConfigTest : public ::testing::Test
{
protected:
	void SetUp() override
	{
		Py_Initialize();

	}

	void TearDown() override
	{
		Py_Finalize();
	}
};


TEST_F(ModelConfigTest, emptyConfig)
{

	boost::python::dict dict{};
	const char* imgPath = "imgPath";

	BlurDetector::ModelConfig config{imgPath, dict };
	ASSERT_EQ(config.isValid(), false);
	ASSERT_EQ(config.getImagePath(), imgPath);
	ASSERT_EQ(config.getModelPath(), "INVALID");
	ASSERT_EQ(config.getThreshold(), 0.0);
	ASSERT_EQ(config.getVisualizationPath(), "INVALID");
	ASSERT_EQ(config.shouldCreateDetailedImage(), false);

}

TEST_F(ModelConfigTest, lackOfKeys_1)
{

	boost::python::dict dict{};
	dict["modelPath"] = "modelPath";
	const char* imgPath = "imgPath";

	BlurDetector::ModelConfig config{ imgPath, dict };
	ASSERT_EQ(config.isValid(), false);
	ASSERT_EQ(config.getImagePath(), imgPath);
	ASSERT_EQ(config.getModelPath(), "modelPath");
	ASSERT_EQ(config.getThreshold(), 0.0);
	ASSERT_EQ(config.getVisualizationPath(), "INVALID");
	ASSERT_EQ(config.shouldCreateDetailedImage(), false);

}

TEST_F(ModelConfigTest, lackOfKeys_2)
{

	boost::python::dict dict{};
	dict["modelPath"] = "modelPath";
	const char* imgPath = "imgPath";
	dict["thresh"] = "0.5";

	BlurDetector::ModelConfig config{ imgPath, dict };
	ASSERT_EQ(config.isValid(), true);
	ASSERT_EQ(config.getImagePath(), imgPath);
	ASSERT_EQ(config.getModelPath(), "modelPath");
	ASSERT_EQ(config.getThreshold(), 0.5);
	ASSERT_EQ(config.getVisualizationPath(), "INVALID");
	ASSERT_EQ(config.shouldCreateDetailedImage(), false);

}

TEST_F(ModelConfigTest, emptyVisualizationPath)
{

	boost::python::dict dict{};
	dict["modelPath"] = "modelPath";
	const char* imgPath = "imgPath";
	dict["thresh"] = "0.5";
	dict["visualization"] = "";

	BlurDetector::ModelConfig config{ imgPath, dict };
	ASSERT_EQ(config.isValid(), true);
	ASSERT_EQ(config.getImagePath(), imgPath);
	ASSERT_EQ(config.getModelPath(), "modelPath");
	ASSERT_EQ(config.getThreshold(), 0.5);
	ASSERT_EQ(config.getVisualizationPath(), "");
	ASSERT_EQ(config.shouldCreateDetailedImage(), true);

}

TEST_F(ModelConfigTest, validConfig)
{

	boost::python::dict dict{};
	dict["modelPath"] = "modelPath";
	const char* imgPath = "imgPath";
	dict["thresh"] = "0.5";
	dict["visualization"] = "dir";

	BlurDetector::ModelConfig config{ imgPath, dict };
	ASSERT_EQ(config.isValid(), true);
	ASSERT_EQ(config.getImagePath(), imgPath);
	ASSERT_EQ(config.getModelPath(), "modelPath");
	ASSERT_EQ(config.getThreshold(), 0.5);
	ASSERT_EQ(config.getVisualizationPath(), "dir");
	ASSERT_EQ(config.getImageName(), imgPath);
	ASSERT_EQ(config.shouldCreateDetailedImage(), true);
}

TEST_F(ModelConfigTest, thresholdOutOfRange)
{

	boost::python::dict dict{};
	dict["modelPath"] = "modelPath";
	const char* imgPath = "imgPath";
	dict["thresh"] = "1.2";
	dict["visualization"] = ".";

	BlurDetector::ModelConfig config{ imgPath, dict };
	ASSERT_EQ(config.isValid(), false);
	ASSERT_EQ(config.getImagePath(), imgPath);
	ASSERT_EQ(config.getModelPath(), "modelPath");
	ASSERT_EQ(config.getThreshold(), 1.2);
	ASSERT_EQ(config.getVisualizationPath(), "INVALID");
	ASSERT_EQ(config.shouldCreateDetailedImage(), false);
}

TEST_F(ModelConfigTest, thresholdOutOfRange_2)
{

	boost::python::dict dict{};
	dict["modelPath"] = "modelPath";
	const char* imgPath = "imgPath";
	dict["thresh"] = "-0.2";

	BlurDetector::ModelConfig config{ imgPath, dict };
	ASSERT_EQ(config.isValid(), false);
	ASSERT_EQ(config.getImagePath(), imgPath);
	ASSERT_EQ(config.getModelPath(), "modelPath");
	ASSERT_EQ(config.getThreshold(), -0.2);
	ASSERT_EQ(config.getVisualizationPath(), "INVALID");
	ASSERT_EQ(config.shouldCreateDetailedImage(), false);
}

TEST_F(ModelConfigTest, getImageName)
{
	

	std::vector<std::string> names = { "\\lala/image.jpg", "\\lala\\image.jpg", "/lala\\image.jpg", "/lala/image.jpg",
		"./image.jpg", "/image.jpg", "image.jpg" };
	for (auto& name : names)
	{
		boost::python::dict dict{};
		BlurDetector::ModelConfig config(name, dict);
		ASSERT_EQ(config.getImageName(), "image.jpg");
	}
}


int main(int argc, char** argv)
{
	::testing::InitGoogleTest(&argc, argv);
	return RUN_ALL_TESTS();
}
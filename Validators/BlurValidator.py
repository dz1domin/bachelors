import pandas as pd
import xml.etree.ElementTree as ET
from Validators.Validator import Validator


class BlurValidator(Validator):

    @staticmethod
    def _load_and_parse_data(input):
        extension = ''.join(input).split('.')[-1]

        if extension == "xlsx":
            data =  pd.read_excel(input, sheet_name=None)
            imges = []
            for sheet in list(data.values()):
                if not sheet.empty:
                    imges.extend(sheet.values.tolist())
            return extension, imges

        elif extension == "json":
            return extension, pd.read_json(input).values

        elif extension == "xml":
            data = ET.parse(input).getroot()
            imges = []
            for node in data:
                imgList = [ img.text for img in node]
                imges.append(imgList)
            return extension, imges
        else:
            print("Not supported file format: " + extension)
            return None, None

    @staticmethod
    def _generate_raport(results, extension):

        if extension == "xlsx":
            results = pd.DataFrame(results, columns = ["image", "label", "classification"])
            results.to_excel("validation_result.xlsx", index = None, header = True)

        elif extension == "json":
            results = pd.DataFrame(results, columns = ["image", "label", "classification"])
            results.to_json("validation_result.json", orient='split', index = False)

        elif extension == "xml":
            result = ET.Element('raport')
            for img, label, classification in results:
                subelem = ET.SubElement(result, 'image')
                ET.SubElement(subelem, 'path').text = str(img)
                ET.SubElement(subelem, 'label').text = str(label)
                ET.SubElement(subelem, 'classification').text = str(classification)
            ET.ElementTree(result).write("validation_result.xml")
        else:
            print("Not supported file format: " + extension)

    @staticmethod
    def _extract_only_name(name):
        option_1 = name.rfind("\\")
        option_2 = name.rfind("/")
        if option_1 != -1 or option_2 != -1:
            return name[ option_1 + 1 if option_1 > option_2 else option_2 + 1: ]
        else:
            return name


    @staticmethod
    def validate(validationFile, moduleResults, moduleOptions):

        moduleResults =  { BlurValidator._extract_only_name(x): 0 if y == 'True' else 1 for x, y in moduleResults }
        extension, data = BlurValidator._load_and_parse_data(validationFile)

        if extension is not None and data is not None:
            data = { x: y for x, y in data}

            validationResult = []
            validClassifications = 0
            allClassifications = 0

            for key, value in moduleResults.items():
                if key in data.keys():
                    validationResult.append([key, data[key], value])
                    if data[key] == value:
                        validClassifications += 1
                    allClassifications += 1

            BlurValidator._generate_raport(validationResult, extension)
            print("Accuracy of model: {}%".format((validClassifications / allClassifications) * 100))
        
    
import pandas as pd
import xml.etree.ElementTree as ET



def _detect_file_extension_and_get_data_as_dict(input):
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
        print("Not supported file format")
        return None, None

def _save_result_of_validation_to_file(results, extension):

    if extension == "xlsx":
        results = pd.DataFrame(results, columns = ["image", "label", "classification"])
        results.to_excel("raport.xlsx", index = None, header = True)

    elif extension == "json":
        results = pd.DataFrame(results, columns = ["image", "label", "classification"])
        results.to_json("raport.json", orient='split', index = False)

    elif extension == "xml":
        result = ET.Element('raport')
        for img, label, classification in results:
            subelem = ET.SubElement(result, 'image')
            ET.SubElement(subelem, 'path').text = str(img)
            ET.SubElement(subelem, 'label').text = str(label)
            ET.SubElement(subelem, 'classification').text = str(classification)
        ET.ElementTree(result).write("raport.xml")
    else:
        assert("This shouldn't be executed")

def validate(filePath, method, methodOptions):
    extension, data = _detect_file_extension_and_get_data_as_dict(filePath)
    if extension is not None and data is not None:
        validationResult = []
        validClassifications = 0

        for img, label in data:
            
            _, result = method(str(img), methodOptions)
            result = 1 if result == 'True' else 0

            validationResult.append([img, label, 1 if result == int(label) else 0])
            if result == int(label):
                validClassifications += 1
        
        _save_result_of_validation_to_file(validationResult, extension)
        print("Accuracy of model: {}%".format((validClassifications / len(data)) * 100))
    
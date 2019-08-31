# @author Dominik Dziuba/Milosz Filus

# History of changes:
# Version      Author      -   Change
# v1           Dominik         Initial version
# v2           Milosz          Add functions checkIfDestinationFolderExistsAndCreateIfNecessary,
#                              getAPIKeyFromUserIfNeeded, cleanAfterRequestFailure


import requests
import urllib.parse
import os

# example version if one wants to manually pass API response for downloading images
# with open('exampleSearchQuery.json', 'r') as file:
#     data = json.load(file)
#     for el in data['hits']:
#         img = el
#         imgURI = img["previewURL"]
#         imgURI = imgURI.replace(' ', '')[:-8].upper() + '_960_720.jpg'
#         imgURI = imgURI.lower()
#         print(imgURI)
#         res = requests.get(imgURI)
#         outFile = open('img_' + str(k) + '.jpg', 'wb')
#         outFile.write(res.content)
#         k += 1
#         res.close()


STORAGE_OF_IMAGES_PATH = '../Images'
STORED_API_KEY_PATH = 'temp/api_key.key'
TEMP_PATH = 'temp'
REQUEST_FAILURE = -1

def checkIfDestinationFolderExistsAndCreateIfNecessary(path):
    if not os.path.exists(path) or not os.path.isdir(path):
        os.mkdir(path)

def getAPIKeyFromUserIfNeeded():
    if not (os.path.exists(STORED_API_KEY_PATH) and os.path.isfile(STORED_API_KEY_PATH)):
        apiKey = input('paste your pixabay API key:\n')
        os.mkdir('temp')
        with open(STORED_API_KEY_PATH, 'w') as apiKeyFile:
            apiKeyFile.write(apiKey)
    else:
        with open(STORED_API_KEY_PATH, 'r') as apiKeyFile:
            apiKey = apiKeyFile.readline()
    return apiKey

def cleanAfterRequestFailure():
    os.remove(STORED_API_KEY_PATH)
    os.rmdir(TEMP_PATH)

def download(apiKey, query, pageNum, k):
    myURL = 'https://pixabay.com/api/?' + urllib.parse.urlencode({'key': apiKey, 'q': query, 'image_type': 'photo', 'page': str(pageNum + 1)})
    print('final URL: ' + str(myURL) + '\n')
    res = requests.get(myURL)

    if 'application/json' in res.headers.get('content-type'):
        data = res.json()
    else:
        print('Request failure, retype your api key')
        return REQUEST_FAILURE, 0

    for hit in data['hits']:
        imgURI = hit["previewURL"]
        imgURI = imgURI.replace(' ', '')[:-8].upper() + '_960_720.jpg'
        imgURI = imgURI.lower()
        print(imgURI)
        res = requests.get(imgURI)
        outFileName = STORAGE_OF_IMAGES_PATH + '/img_' + str(k) + '.jpg'
        while os.path.isfile(outFileName):
            k += 1
            outFileName = STORAGE_OF_IMAGES_PATH + '/img_' + str(k) + '.jpg'
        outFile = open(outFileName, 'wb')
        outFile.write(res.content)
        k += 1
        res.close()
    return len(data['hits']), k


checkIfDestinationFolderExistsAndCreateIfNecessary(STORAGE_OF_IMAGES_PATH)
apiKey = getAPIKeyFromUserIfNeeded()
while True:
    query = input('type your query in:\n')
    p = 0
    downloadedData, currentIndex = download(apiKey, query, p, 0)
    if(downloadedData == REQUEST_FAILURE):
        cleanAfterRequestFailure()
        apiKey = getAPIKeyFromUserIfNeeded()
    else:
        print(downloadedData)
        while downloadedData > 0:
            p += 1
            downloadedData, currentIndex = download(apiKey, query, p, currentIndex + 1)

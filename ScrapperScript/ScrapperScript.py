# @author Dominik Dziuba

import requests
import urllib.parse

k = 0

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

apiKey = input('paste your pixabay API key:\n')
while True:
    query = input('type your query in:\n')
    myURL = 'https://pixabay.com/api/?' + urllib.parse.urlencode({'key': apiKey, 'q': query, 'image_type': 'photo'})
    print('final URL: ' + str(myURL) + '\n')
    res = requests.get(myURL)
    data = res.json()
    for hit in data['hits']:
        imgURI = hit["previewURL"]
        imgURI = imgURI.replace(' ', '')[:-8].upper() + '_960_720.jpg'
        imgURI = imgURI.lower()
        print(imgURI)
        res = requests.get(imgURI)
        outFile = open('img_' + str(k) + '.jpg', 'wb')
        outFile.write(res.content)
        k += 1
        res.close()
import requests
import json

k = 0

with open('searchQuery.json', 'r') as file:
    data = json.load(file)
    for el in data['hits']:
        img = el
        imgURI = img["previewURL"]
        imgURI = imgURI.replace(' ', '')[:-8].upper() + '_960_720.jpg'
        imgURI = imgURI.lower()
        print(imgURI)
        res = requests.get(imgURI)
        outFile = open('img_' + str(k) + '.jpg', 'wb')
        outFile.write(res.content)
        k += 1
        res.close()
    print(len(data['hits']))
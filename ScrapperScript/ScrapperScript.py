# @author Dominik Dziuba

import requests
import urllib.parse

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


def download(apiKey, query, pageNum, k):
    myURL = 'https://pixabay.com/api/?' + urllib.parse.urlencode({'key': apiKey, 'q': query, 'image_type': 'photo', 'page': str(pageNum + 1)})
    print('final URL: ' + str(myURL) + '\n')
    res = requests.get(myURL)

    if 'application/json' in res.headers.get('content-type'):
        data = res.json()
    else:
        return 0, 0

    for hit in data['hits']:
        imgURI = hit["previewURL"]
        imgURI = imgURI.replace(' ', '')[:-8].upper() + '_960_720.jpg'
        imgURI = imgURI.lower()
        print(imgURI)
        res = requests.get(imgURI)
        outFile = open('../Images/img_' + str(k) + '.jpg', 'wb')
        outFile.write(res.content)
        k += 1
        res.close()
    return len(data['hits']), k

apiKey = input('paste your pixabay API key:\n')
while True:
    query = input('type your query in:\n')
    p = 0
    res = download(apiKey, query, p, 0)
    while res[0] > 0:
        p += 1
        res = download(apiKey, query, p, res[1] + 1)

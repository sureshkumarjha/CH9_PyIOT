import requests
import webbrowser

filePath = 'Jefin.jpeg'
searchUrl = 'https://in.linkedin.com/in/jefin-francis
multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
response = requests.post(searchUrl, files=multipart, allow_redirects=False)
fetchUrl = response.headers['Location']
print(fetchUrl)
webbrowser.open(fetchUrl)


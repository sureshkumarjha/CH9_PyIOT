# extract and plot each detected face in a photograph
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from matplotlib.patches import Circle
from mtcnn.mtcnn import MTCNN
from PIL import Image
from SSIM_PIL import compare_ssim
import numpy as np
from matplotlib import cm
import face_recognition
from newit import*
import os
import glob
 
from icrawler.builtin import BingImageCrawler
from six.moves.urllib.parse import urlparse
from icrawler import ImageDownloader
import base64




urls  = []
class MyImageDownloader(ImageDownloader):

    def get_filename(self, task, default_ext):
        z = task['file_url']
        url_path = urlparse(task['file_url'])[2]
        urls.append(z)

        if '.' in url_path:
            extension = url_path.split('.')[-1]
            if extension.lower() not in [
                    'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'gif', 'ppm', 'pgm'
            ]:
                extension = default_ext
        else:
            extension = default_ext
        # works for python3
        filename = base64.b64encode(url_path.encode()).decode()
        return '{}.{}'.format(filename, extension)

def crawl_it(name_to_search):
    google_crawler = BingImageCrawler(
    feeder_threads=1,
    parser_threads=2,
    downloader_threads=4,
    downloader_cls=MyImageDownloader,
    storage={'root_dir': 'images/google'})
    google_crawler.crawl(keyword=name_to_search,  max_num=20, file_idx_offset=0)
    

	



# draw each face separately
def draw_faces(filename, result_list,result_list_2,compare_file):
	# load the image
	im_new = Image.open(filename) 
	data = pyplot.imread(filename)
	im1 = Image.open(compare_file) 
	x_1, y_1, width_1, height_1 = result_list_2[0]['box']
	x_2, y_2 = x_1 + width_1, y_1 + height_1
	im1 = im1.crop((x_1, y_1, x_2,y_2))
	flag = 0
	# plot each face as a subplot
	for i in range(len(result_list)):
		# get coordinates
			x1, y1, width, height = result_list[i]['box']
			x2, y2 = x1 + width, y1 + height
		# define subplot
			pyplot.subplot(1, len(result_list), i+1)
			pyplot.axis('off')
			z = data[y1:y2, x1:x2]
			im_new_1 = im_new.crop((x1, y1, x2,y2))
			im_new_1.save("temp.jpg")
			picture_of_me = face_recognition.load_image_file(compare_file)
			my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

	# my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!

			unknown_picture = face_recognition.load_image_file(filename)
			unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

	# Now we can see the two face encodings are of the same person with `compare_faces`!

			results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)
			if results[0] == True:
				print("It's a picture of me!")
				flag = 1

			else:
				print("It's not a picture of me!")

	''' 
	if flag > 0:
		print("present in the picture")
	else:
		print("not present in the picture")
	'''
	return flag

		
# show the output image
remv = None
def find_it_google(compare_file,path,name_to_search):
	#files = [f for f in glob.glob(path + "**/*.jpg", recursive=True)]
	list_url = []
	#print(files)
	# load image from file
	crawl_it(name_to_search)

	files = [f for f in glob.glob(path + "**/*.jpg", recursive=True)]
	# display faces on the original image
	
	print(len(files),len(urls))

	for fi in range(len(files)):
		pixels = pyplot.imread(files[fi])
		pixel_it = pyplot.imread(compare_file)
		im2 = Image.open(files[fi]) 
	# create the detector, using default weights
		detector = MTCNN()
	# detect faces in the image
		faces = detector.detect_faces(pixels)
		faces_2 = detector.detect_faces(pixel_it)
		flag_1 = draw_faces(files[fi], faces, faces_2,compare_file)
		print(flag_1)
		if flag_1 > 0:
				list_url.append(urls[fi])
	return list_url 

path = r'C:\Users\parth\Desktop\face_it\images\google'


image_urls = find_it_google(r'bar_it_2.jfif',r'C:\Users\parth\Desktop\face_it\images\google',r'Obama')
print(image_urls)

urls = []

for f in glob.glob(path + "**/*.jpg"):
	os.remove(f)



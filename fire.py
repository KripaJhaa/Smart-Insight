import pyrebase
import cv2
import numpy as np
import imageio
import time
import urllib
import json
import requests



def fireBaseCon(firebase):
	print('Connecting Firebase..')
	
  	# Get a reference to the auth service
	auth = firebase.auth()

	# Log the user in
	email = 'prajwaloggy15@gmail.com'
	password = 'prajwalpanda15'
	user = auth.sign_in_with_email_and_password(email, password)
	print('Connected..')
	return user
	# print(auth.get_account_info(user['idToken']))

def uploadImage(firebase,user):
	storage = firebase.storage()
	# as admin
	storage.child("images/water.jpg").put('water.jpg',user['idToken'])
	print('Done Uploading..')

def downloadImage(firebase,user):
	print('Downloading Start..')
	storage = firebase.storage()
	# storage.child("images/example.jpg").download("example.jpg")
	print(storage.child("images/example.jpg").get_url(0))
	image=urllib.URLopener()
	image.retrieve(storage.child("images/example.jpg").get_url(1),'example.jpg')

	print('Downloading End..')

def getLoc():
	send_url = 'http://freegeoip.net/json'
	r = requests.get(send_url)
	j = json.loads(r.text)
	lat = j['latitude']
	lon = j['longitude']
	return (lat,lon)

if __name__ == '__main__':
	print('Start')
	try:
		waterClassifier = cv2.CascadeClassifier('haarcascade_car.xml')
		
		config = {
	    "apiKey": "AIzaSyCbTlgMcL6PulNOYzz7y1Mbx9WEEArVuGw",
	    "authDomain": "smart-8bc21.firebaseapp.com",
	    "databaseURL": "https://smart-8bc21.firebaseio.com",
	    "projectId": "smart-8bc21",
	    "storageBucket": "smart-8bc21.appspot.com",
	    "messagingSenderId": "332802746419"
	  	}
	  	firebase = pyrebase.initialize_app(config)
	  	user = fireBaseCon(firebase)
	  	loc = getLoc()

	  	print('Wait..')
		filename = 'cars.avi'
		
		vid = imageio.get_reader(filename,  'ffmpeg')
		# nums = [0, 300]

		for img in vid:
			
			# downloadImage(firebase,user)
			# img = cv2.imread('example.jpg')
			# cv2.imshow('Live Feed',img)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			flag = 0	
			lower_range = np.array([0, 0, 0])
			upper_range = np.array([120, 10, 230])
			originalImage = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
			hsvImage = cv2.cvtColor(originalImage,cv2.COLOR_BGR2HSV)
			filterImage = cv2.inRange(hsvImage,lower_range,upper_range)
			ksize = 3
			kernel = np.ones((ksize,ksize),dtype='uint8')
			filterImage = cv2.dilate(filterImage,kernel,iterations=10)
			filterImage = cv2.erode(filterImage,kernel,iterations=10)
			foriginalImage = cv2.bitwise_and(originalImage,originalImage,mask =  filterImage)
			grayfImage = cv2.cvtColor(foriginalImage,cv2.COLOR_BGR2GRAY)
			water = waterClassifier.detectMultiScale(grayfImage,1.3,5)
			for x,y,w,h in water:
				cv2.rectangle(foriginalImage,(x,y),(x+w,y+h),(0,0,255),2)
				cv2.imshow('example.jpg',foriginalImage)
				cv2.waitKey(300)
				db = firebase.database()
				# data to save
				data = {
				    "lati": str(loc[0]),
				    "long" : str(loc[1])
				}
				# Pass the user's idToken to the push method
				db.child("users").push(data)
				# results = db.child("users").push(data, user['idToken'])
				print('Problem Detected!! Message Trigger!!')
				cv2.imwrite('water.jpg',foriginalImage)
				uploadImage(firebase,user)
				# users = db.child("users").get()
				# print(users.val())
				print('Done..')
				flag = 1
				break
			cv2.imshow('example.jpg',foriginalImage)
			if flag:
				cv2.destroyAllWindows()
				break	

			# originalImage = cv2.cvtColor(num,cv2.COLOR_RGB2BGR)
			# grayImage = cv2.cvtColor(originalImage,cv2.COLOR_BGR2GRAY)

			# cannyImage = cv2.Canny(grayImage,50,120)

			# contour,_ = cv2.findContours(cannyImage,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

			# if len(contour)>=1:
			# 	db = firebase.database()
			# 	# data to save
			# 	data = {
			# 	    "lati": str(loc[0]),
			# 	    "long" : str(loc[1])
			# 	}
			# 	# Pass the user's idToken to the push method
			# 	results = db.child("users").push(data, user['idToken'])
			# 	print('Environment Virus Found!! Message Trigger!!')
			# 	cv2.imwrite('example.jpg',originalImage)
			# 	uploadImage(firebase,user)
			# 	break
			# time.sleep(100)

		print('End..')
	except:
		print('Problem Occur!!')	
import sys
import cv2
import numpy as np
from django.http import StreamingHttpResponse, HttpResponse
from django.views.decorators import gzip
from PIL import ImageGrab
from template_matching.template import match_template
from AR.AR_aruco import ar_aruco_detect


class VideoCamera(object):
	def __init__(self):
		self.frame = None
		self.res1 = float()
		self.res2 = float()
		self.feed1 = str()
		self.feed2 = str()
		self.num_step = 5
		self.curr_step = 1
		self.threshold = [0.8 ,0.85, 0.85, 0.85, 0.8]
		self.AR_marker_name = ["AR-1.jpg","AR-10.jpg","AR-11.jpg","AR-12.jpg","AR-13.jpg"]
		self.complete_count = 0
		self.flag = False

	def get_frame(self):
		self.update()
		image = self.frame
		ret, jpeg = cv2.imencode('.jpg', image)
		return jpeg.tobytes()

	def add_ar_marker(self, frame, curr_step):
		ar_marker = cv2.imread(self.AR_marker_name[curr_step-1])
		scale_percent = 15 # percent of original size
		width = int(ar_marker.shape[1] * scale_percent / 100)
		height = int(ar_marker.shape[0] * scale_percent / 100)
		dim = (width, height)
		ar_marker = cv2.resize(ar_marker, dim, interpolation = cv2.INTER_AREA)
		frame[:ar_marker.shape[0],frame.shape[1]-ar_marker.shape[1]:] = ar_marker
		return frame

	def update(self):
		self.frame = ImageGrab.grab(bbox=(310,135,1280,640)) # bbox specifies specific region (bbox= x,y,width,height)
		self.frame = np.array(self.frame)
		self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
		self.frame, self.flag = ar_aruco_detect(self.frame, self.flag)
		if self.curr_step <= self.num_step:
			if self.curr_step != self.num_step:
				if self.flag:
					self.frame = self.add_ar_marker(self.frame, self.curr_step)
				left_frame = self.frame[:, 0:int(self.frame.shape[1] / 2)]
				right_frame = self.frame[:, int(self.frame.shape[1] / 2):]
				self.feed1, self.res1 = match_template(left_frame, self.curr_step, self.threshold[self.curr_step-1])
				self.feed2, self.res2 = match_template(right_frame, self.curr_step, self.threshold[self.curr_step-1])
				print(self.curr_step,". ", self.feed1, self.res1, self.feed2, self.res2)
				if self.feed1 == "OK" and self.feed2 == "OK":
					self.curr_step += 1
			else:
				if self.complete_count < 500:
					self.complete_count += 1
					if self.flag:
						self.frame = self.add_ar_marker(self.frame, self.curr_step)
					print(self.curr_step, ". Assemble the screws")
				else:
					self.curr_step += 1
		else:
			print ("Assembly Completed")


cam = VideoCamera()
frame = np.uint8(np.zeros([640,480]))

def hello(request):
	text = "<h1>welcome to my app number!</h1>"
	return HttpResponse(text)


def gen(camera):
	global frame
	while True:
		frame = camera.get_frame()
		yield(b'--frame\r\n'
			b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livefe(request):
	print("Session Started:")
	try:
		return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
	except KeyboardInterrupt:
		sys.exit()
	except:
		print("not able to send")


def ar_marker():
	global frame
	while True:
		yield(b'--frame\r\n'
			b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def livefe1(request):
	print("Session 1 Started:")
	try:
		return StreamingHttpResponse(ar_marker(), content_type="multipart/x-mixed-replace;boundary=frame")
	except KeyboardInterrupt:
		sys.exit()
	except:
		print("not able to send")
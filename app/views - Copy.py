import sys
import cv2
import numpy as np
from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse
from django.views.decorators import gzip
#import gzip

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        #threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        print("updating")
        self.update()
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        (self.grabbed, self.frame) = self.video.read()


cam = VideoCamera()

def hello(request):
   text = "<h1>welcome to my app number!</h1>"
   return HttpResponse(text)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def livefe(request):
    print("as")
    try:
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        print("not able to send")  # This is bad! replace it with proper handling
        pass

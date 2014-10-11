from Tkinter import Tk
from human_activity_interface import HumanActivityInterface
import matplotlib.pyplot as plt
import numpy as np
import cv2
from datetime import datetime

class Motion(HumanActivityInterface):
	def __init__(self,master):
		HumanActivityInterface.__init__(self,master)
		
		self.color = plt.get_cmap('gray')
		self.backgroundFrame = None
		self.device = "http://192.168.1.104/asp/video.cgi?.mjpeg"
		#self.device = 0
		self.count  = 0
		self.timer.add_callback(self.eventDetection)
		self.captureVideo()
		self.bufferImages = []
		
	def captureVideo(self):
		self.cap = cv2.VideoCapture()
		self.cap.open(self.device)
		ret, frame = self.cap.read()
		self.frameArea = frame.shape[0]*frame.shape[1]
		grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
		self.videoImageHandler = self.videoAxis.imshow(grayFrame,self.color)
		self.backgroundImageHandler = self.backgroundAxis.imshow(grayFrame,self.color)
		self.differenceImageHandler = self.differenceAxis.imshow(grayFrame,self.color)
		self.countourImageHandler = self.countourAxis.imshow(grayFrame,self.color)
	
	def eventDetection(self):
		frame,grayFrame = self.readFrames()
		if len(frame) > 0:
			differenceFrame = self.calculateDifference(grayFrame)
			self.backgroundFrame = self.calculateBackground(grayFrame,self.backgroundFrame)
			self.thresholdingAndContour(differenceFrame,frame)
		
	def eventSave(self,bufferFrame,videowriter):
		cnt = len(bufferFrame)
		for i in range(0,cnt):
			videowriter.write(bufferFrame[i])
		
	def readFrames(self):
		flag, frame = self.cap.read()
		if flag == True:
			grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			self.videoImageHandler.set_array(grayFrame)
			self.videoCanvas.draw()
			return frame,grayFrame
		else:
			print "Not streaming"	
			return [],[]
		
	def calculateDifference(self,grayFrame):
		if self.backgroundFrame == None:
			self.backgroundFrame = grayFrame
		differenceFrame = abs(np.subtract(grayFrame,self.backgroundFrame))
		self.differenceImageHandler.set_array(differenceFrame)
		self.differenceCanvas.draw()
		return differenceFrame

	def calculateBackground(self,grayFrame,backgroundFrame):
		self.backgroundImageHandler.set_array(backgroundFrame)
		self.backgroundCanvas.draw()
		coefficient = float(self.coefficientEntry.get())
		background = np.add(np.multiply((1-coefficient),backgroundFrame), np.multiply(coefficient,grayFrame))
		return background

	def thresholdingAndContour(self,diffFrame,frame):
		thresholdedFrame  = cv2.inRange(diffFrame,np.array(10), np.array(50))
		contours, hierarchy = cv2.findContours(thresholdedFrame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
				
		if len(contours) > 0: 
			areas = [cv2.contourArea(c) for c in contours]
			index = np.argmax(areas)
			contourMaxArea = contours[index]
			cv2.drawContours(frame, [contourMaxArea], 0, (0,0,0), 3)
			self.countourImageHandler.set_array(frame)
			self.countourCanvas.draw()
			
			if max(areas) >= (self.frameArea/4):
				self.count += 1
				if self.count > 6:
					self.eventLabel["text"] = "Events:-" + str(self.count)
					self.bufferImages.append(frame)
					self.currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			else :
				if self.bufferImages != []:
					fourcc = cv2.cv.CV_FOURCC(*'PIM1')
					videowriter = cv2.VideoWriter(str(self.currentTime)+'.mpeg',fourcc, 25, (640,480))
					self.eventSave(self.bufferImages,videowriter)
					self.bufferImages = []
					del(videowriter)
									
			
if __name__ == "__main__":
	root = Tk()
	Motion(root)
	root.mainloop()

	

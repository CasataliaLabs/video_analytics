from Tkinter import Tk	
from human_activity_interface import HumanActivityInterface
import matplotlib.pyplot as plt
import numpy as np
import cv2
from datetime import datetime
import time
plt.ion()

class Motion(HumanActivityInterface):
	def __init__(self,master):
		
		HumanActivityInterface.__init__(self,master)
		self.color = plt.get_cmap('gray')
		self.backgroundFrame = None
		self.count  = 0
		self.bufferImages = []
		self.device = "http://192.168.1.104/asp/video.cgi?.mjpeg"
		self.timer.add_callback(self.eventDetection)
		self.buttonTrain.bind("<Key>",self.trainZone)
		self.zoneArea = None
		grayFrame = self.captureVideo()
		self.setImageHandlers(grayFrame)
		self.mean =0
		self.variance=0
		self.contourMaxArea=0
		self.doorExit='UP' # Set UP , DOWN, LEFT , RIGHT according to the position of the door with respect to the camera
	
	def trainZone(self,event):
		if  str(event.keysym) == 'space':
			flag, frame = self.cap.read()
			if flag == True:
				#~ grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				plt.imshow(frame)
				self.mask = np.zeros(frame.shape[:2],dtype = 'uint8')
				zoneArea = np.floor(plt.ginput(n=0, timeout=-1, show_clicks=True))
				self.zoneArea = zoneArea.astype('int')
				cv2.drawContours(frame,[self.zoneArea],0,255,3)
				cv2.drawContours(self.mask,[self.zoneArea],0,255,-1)
				plt.imshow(self.mask,self.color)
				

			
	# Capture Videos	
	def captureVideo(self):
		
		self.cap = cv2.VideoCapture()
		camIsOpen = self.cap.open(self.device)
		
		if camIsOpen:
			ret, frame = self.cap.read()
			self.frameArea = frame.shape[0]*frame.shape[1]
			grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			return grayFrame
		else:
			print "Error:- CAM is not opened.Please check the connection"
			return None
	
	# Define Image Handlers		
	def setImageHandlers(self,grayFrame):
		if self.cap.isOpened():
			self.countourImageHandler = self.countourAxis.imshow(grayFrame,self.color)
			self.videoImageHandler = self.videoAxis.imshow(grayFrame,self.color)
	
	# Detect Events
	def eventDetection(self):
		tic = time.time()
		frame,grayFrame = self.readFrames()
		if len(frame) > 0:
			differenceFrame = self.calculateDifference(grayFrame)
			self.backgroundFrame = self.calculateBackground(grayFrame)
			self.thresholdingAndContour(differenceFrame,frame)
			self.showData(tic)
			#~ print "Total Time:-",time.time() - tic
		else:
			print 'else loop line 61 in operation'
		
	def showData(self,tic):
		self.dataAxis.clear()
		self.dataAxis=self.dataFig.gca()
		self.dataAxis.set_axis_off()
		
		toc = '{0:.3f}'.format(time.time() -tic)
		self.mean = '{0:.3f}'.format(float(self.mean))
		self.variance='{0:.3f}'.format(float(self.variance))
		
		values=[['Mean',self.mean],['Variance',self.variance],['Total Ex',toc],['Contour',self.contourMaxArea]]
		t = self.dataAxis.table(cellText=values,colWidths = [.2, .1],cellLoc='left',loc='center')
		t.scale(3, 3)
		self.dataCanvas.show()         
		
		if self.zoneArea != None:
			# Writing to a  text file	
			fo = open("log1.txt","a")
			fo.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\t Mean:- '+self.mean+'\t Variance:- '+self.variance+'\t Max Area:- '+str(self.contourMaxArea)+'\n')
			fo.close()
                  
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
			print "Error:- CAM not streaming"	
			return [],[]
		
	def calculateDifference(self,grayFrame):
		
		if self.backgroundFrame == None:
			self.backgroundFrame = grayFrame
		differenceFrame = abs(np.subtract(grayFrame,self.backgroundFrame))
		#~ differenceFrame = abs(grayFrame - self.backgroundFrame)
		
		return differenceFrame

	def calculateBackground(self,grayFrame):
		coefficient = float(self.coefficientEntry.get())
		background = np.add(np.multiply((1-coefficient),self.backgroundFrame), np.multiply(coefficient,grayFrame))
		#~ background = ((1-coefficient) * self.backgroundFrame) + (coefficient * grayFrame)
		return background

	def thresholdingAndContour(self,diffFrame,frame):
		#~ tic = time.time()
		if self.zoneArea != None:
				colMin = np.min(self.zoneArea[:,0])
				colMax = np.max(self.zoneArea[:,0])
				rowMin = np.min(self.zoneArea[:,1])
				rowMax = np.max(self.zoneArea[:,1])
				#~ box = (xmin,xmax,ymin,ymax)
				self.croppedFrame = frame[rowMin:rowMax,colMin:colMax]
				#~ self.croppedFrame=frame.crop(box)
				self.mean = self.croppedFrame.mean()
				self.variance = np.var(self.croppedFrame)				 										
				#~ moments = cv2.moments(np.asarray(self.zoneArea,dtype=np.uint8))
				#~ variance1 = moments['mu02']
				#~ variance2 = moments['mu20']
				
				cv2.drawContours(frame, [self.zoneArea], 0 , 255, 3)
				
		thresholdedFrame  = cv2.inRange(diffFrame,np.array(10), np.array(50))
		contours, hierarchy = cv2.findContours(thresholdedFrame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		self.c = contours
		if len(contours) > 0: 
			areas = [cv2.contourArea(c) for c in contours]
			index = np.argmax(areas)
			contourMaxArea = contours[index]
			self.contourMaxArea=cv2.contourArea(contourMaxArea)
			cv2.drawContours(frame, [contourMaxArea], 0 , (0,0,0), 3)
			
			self.countourImageHandler.set_array(frame)
			self.countourCanvas.draw()
			
			if max(areas) >= (self.frameArea/4):
				self.count += 1
				if self.count > 20:
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
		#~ print "ThresholdTime----:-",time.time() - tic							
				
if __name__ == "__main__":
	root = Tk()
	h= Motion(root)
	h.cap.release()
	h.cap.open("http://192.168.1.104/video.cgi")

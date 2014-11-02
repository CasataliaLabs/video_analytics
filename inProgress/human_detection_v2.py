from Tkinter import Tk
from human_detection_interface_v1 import HumanActivityInterface
import matplotlib.pyplot as plt
import numpy as np
import cv2
from datetime import datetime
import time
plt.ion()

class Motion(HumanActivityInterface):
	def __init__(self,master,camUrl):
		
		HumanActivityInterface.__init__(self,master)
		self.color = plt.get_cmap('gray')
		self.backgroundFrame = None
		#~ self.zoneBackground = None
		#~ self.bufferImages = []
		self.device = camUrl
		#~ self.device=0
		self.timer.add_callback(self.eventDetection)
		self.buttonTrain.bind("<Key>",self.trainZone)
		
		grayFrame = self.captureVideo()
		self.setImageHandlers(grayFrame)
		
		self.mean =0
		self.variance=0
		self.contourMaxArea=0
		self.zoneArea = None
		self.threshold = 100
		
		self.hog = cv2.HOGDescriptor()
		self.hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
		
		self.prevTime=0
		self.count =0
		self.meanList=[]
		self.previousFrame = None
		
		#~ self.pnt1=None
		#~ self.pnt2=None
		self.timer.start()

	# Define Image Handlers		
	def setImageHandlers(self,grayFrame):
		if self.cap.isOpened():
			self.countourImageHandler = self.countourAxis.imshow(grayFrame,self.color)
			self.videoImageHandler = self.videoAxis.imshow(grayFrame,self.color)
			
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
	
	def readFrames(self):
		
		flag, frame = self.cap.read()
		if flag == True:
			grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			return frame,grayFrame
		else:
			print "Error:- CAM not streaming"	
			return [],[]		
	
	# Detect Events
	def eventDetection(self):
		tic = time.time()
		frame,grayFrame = self.readFrames()
		if len(frame) > 0:
			differenceFrame = self.calculateDifference(grayFrame)
			#~ self.differenceFrame  = differenceFrame # delete later
			#~ self.backgroundFrame = self.calculateBackground(grayFrame)
			
			
			
			if self.prevTime == 0:
				self.prevTime = time.time()
				#~ 
			if time.time()-self.prevTime > 60:
				self.count = 0
				print max(self.meanList)
				if max(self.meanList) < 100:
					self.backgroundFrame = self.calculateBackground(grayFrame)
#~ 
				self.prevTime = time.time()
				self.meanList = []
			else:
				self.count += 1
				print self.count
				#~ d = abs(np.subtract(grayFrame,self.previousFrame)).mean()
				#~ diff = (np.subtract(grayFrame,self.previousFrame));
				#~ print 'diff.min is :', diff.min()
				grayFrame = np.asarray(grayFrame, 'int')
				self.previousFrame = np.asarray(self.previousFrame, 'int')
				d = abs(np.subtract(grayFrame,self.previousFrame)).mean()
				self.meanList.append(d)
				#~ 
			self.previousFrame = grayFrame	
			
			self.thresholdingAndContour(differenceFrame,frame)
			#~ self.showData(tic)
			
		else:
			print 'else loop line 61 in operation'
				
				
	def calculateDifference(self,grayFrame):
		if self.backgroundFrame == None:
			self.backgroundFrame = grayFrame
			self.previousFrame = grayFrame
		grayFrame = np.asarray(grayFrame, 'int')
		self.backgroundFrame = np.asarray(self.backgroundFrame, 'int')
		differenceFrame = abs(np.subtract(grayFrame,self.backgroundFrame))
		return differenceFrame

	def calculateBackground(self,grayFrame):
		#~ coefficient = float(self.coefficientEntry.get())
		coefficient = 0.05
		background = np.add(np.multiply((1-coefficient),self.backgroundFrame), np.multiply(coefficient,grayFrame))
		return background
			
	#Human Motion detection ------------------------------------------------------------------------------------
	def draw_detections(self,img, rects, thickness = 2):
		for x, y, w, h in rects:
			cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), thickness)
			
	def findPeople(self,frm, rMinrMaxcMincMax):
		img = frm * 1
		rMin = rMinrMaxcMincMax[0]
		rMax = rMinrMaxcMincMax[1]
		cMin = rMinrMaxcMincMax[2]
		cMax = rMinrMaxcMincMax[3]
		rowMinCFrame = rMin
		rowMaxCFrame = img.shape[0]
		colMinCFrame = cMin
		colMaxCFrame = img.shape[1]
		#~ 
		if rMin >= self.threshold:
			rowMinCFrame = rMin-self.threshold
		if rMax + self.threshold <= rowMaxCFrame:
			rowMaxCFrame=rMax+self.threshold
		if cMin >= self.threshold:
			colMinCFrame = cMin - self.threshold
		if cMax + self.threshold <= colMaxCFrame:
			colMaxCFrame = cMax+self.threshold
	
		img = frm[colMinCFrame:colMaxCFrame,rowMinCFrame:rowMaxCFrame]
		
		#~ img = frm[cMin:cMax,rMin:rMax]
		imgRow,imgCol,layers = img.shape
		if (imgRow > 0) and (imgCol > 0):
			if imgRow <= 65:
				imgCol = imgCol * 65 / imgRow
				imgRow = 65
			if imgCol <= 65:
				imgRow = imgRow * 65 /imgCol
				imgCol = 65
			img = np.resize(img,(imgRow,imgCol,3))
			img = np.asarray(img.round(),dtype=np.uint8)
			
			self.found, w = self.hog.detectMultiScale(img, winStride=(8,8), padding=(32,32), scale=1.05)
			self.draw_detections(img, self.found)
			self.videoImageHandler.set_array(img)
			self.videoCanvas.draw()
			
		else:
			print 'imgRow or imgCol is zero'
	# Ending of human motion detection -- -----------------------------------------------------------
	
	
	def trainZone(self,event):
		if  str(event.keysym) == 'space':
			flag, frame = self.cap.read()
			if flag == True:
				#~ grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				plt.imshow(frame)
				#~ self.mask = np.zeros(frame.shape[:2],dtype = 'uint8')
				
				pnt1 = np.int32(plt.ginput(n=0, timeout=-1, show_clicks=True))
				self.pnt1 = pnt1.reshape((-1,1,2))
				
				xMax = max(self.pnt1[:,:,0])[0]
				yMax = max(self.pnt1[:,:,1])[0]
				xMin = min(self.pnt1[:,:,0])[0]
				yMin = min(self.pnt1[:,:,1])[0]
				
				cv2.polylines(frame,[self.pnt1],True,(0,255,255),thickness=3)
				plt.imshow(frame)
				
				pnt2 = np.int32(plt.ginput(n=0, timeout=-1, show_clicks=True))
				self.pnt2 = pnt2.reshape((-1,1,2))
				
				xMax = max(self.pnt2[:,:,0])[0]
				yMax = max(self.pnt2[:,:,1])[0]
				xMin = min(self.pnt2[:,:,0])[0]
				yMin = min(self.pnt2[:,:,1])[0]
				
				cv2.polylines(frame,[self.pnt2],True,(0,255,255),thickness=3)
				plt.imshow(frame)
						
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
	
	def minMaxOfList(self, areas, c):
		cBig = []
		kcCounter = 0
		rMin = []
		rMax = []
		cMin = []
		cMax = []

		for k in areas:
			if k > 100:
				cCurrent = c[kcCounter]
				cBig.append(cCurrent)
				rMin.append(cCurrent[:,:,0].min())
				cMin.append(cCurrent[:,:,1].min())
				rMax.append(cCurrent[:,:,0].max())
				cMax.append(cCurrent[:,:,1].max())
			kcCounter += 1
		if len(cBig) > 0:
			rMin = np.min(rMin)
			rMax = np.max(rMax)
			cMin = np.min(cMin)
			cMax = np.max(cMax)
		self.rMinrMaxcMincMax = [rMin, rMax, cMin, cMax]
		
		return [rMin, rMax, cMin, cMax], cBig

	def thresholdingAndContour(self,diffFrame,frame):
		#~ tic = time.time()
		self.thresholdedFrame = np.asarray(diffFrame > 60,dtype=np.uint8)
		#~ self.thresholdedFrame = cv2.inRange(diffFrame,np.array(30), np.array(255))
		#~ self.normalizedFrame = np.divide(self.thresholdedFrame,255)
		#~ kernel = np.ones((15,5),np.uint8)
		#~ self.final = cv2.erode(self.thresholdedFrame,kernel,iterations = 1)
		#~ self.final = cv2.dilate(self.final,kernel,iterations=1)
		contours, hierarchy = cv2.findContours(self.thresholdedFrame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		
		if len(contours) > 0:
			self.contours = contours
			self.frame = frame
			areas = [cv2.contourArea(c) for c in contours]
			self.areas = areas
			#~ index = np.argmax(areas)
			#~ contourMaxArea = contours[index]
			#~ self.contourMaxArea=cv2.contourArea(contourMaxArea)
			#~ if self.contourMaxArea > 10:
			#~ self.findPeople(frame,contours[index])
			rMinrMaxcMincMax, cBig = self.minMaxOfList(areas, contours)
			if len(cBig) > 0:
				self.findPeople(frame, rMinrMaxcMincMax)
				cv2.drawContours(frame, cBig, -1 , (255,0,0), 3)
			
		self.countourImageHandler.set_array(frame)
		self.countourCanvas.draw()
		
		#~ if (self.pnt1 != None) & (self.pnt2 != None):
			#~ xMax = max(self.pnt1[:,:,0])[0]
			#~ yMax = max(self.pnt1[:,:,1])[0]
			#~ xMin = min(self.pnt1[:,:,0])[0]
			#~ yMin = min(self.pnt1[:,:,1])[0]
		#~ 
			#~ frame[yMin:yMax,xMin:xMax,0] = thresholdedFrame[yMin:yMax,xMin:xMax]
			#~ frame[yMin:yMax,xMin:xMax,1] = thresholdedFrame[yMin:yMax,xMin:xMax]
			#~ frame[yMin:yMax,xMin:xMax,2] = thresholdedFrame[yMin:yMax,xMin:xMax]
		#~ 
			#~ xMax = max(self.pnt2[:,:,0])[0]
			#~ yMax = max(self.pnt2[:,:,1])[0]
			#~ xMin = min(self.pnt2[:,:,0])[0]
			#~ yMin = min(self.pnt2[:,:,1])[0]
			#~ 
			#~ 
			#~ frame[yMin:yMax,xMin:xMax,0] = thresholdedFrame[yMin:yMax,xMin:xMax]
			#~ frame[yMin:yMax,xMin:xMax,1] = thresholdedFrame[yMin:yMax,xMin:xMax]
			#~ frame[yMin:yMax,xMin:xMax,2] = thresholdedFrame[yMin:yMax,xMin:xMax]
			#~ 
		
			
			#~ zone1 = frame[yMin:yMax,xMin:xMax]
			
				# These variables can be set as variables of the class
				#~ colMin = np.min(self.zoneArea[:,0])
				#~ colMax = np.max(self.zoneArea[:,0])
				#~ rowMin = np.min(self.zoneArea[:,1])
				#~ rowMax = np.max(self.zoneArea[:,1])
				#~ Get the zonepoints - get difference embedd in the frame
				
				#~ self.croppedFrame = frame[rowMin:rowMax,colMin:colMax]
				#~ croppedGrayFrame = cv2.cvtColor(h.croppedFrame,cv2.COLOR_BGR2GRAY)
				
				#~ if self.zoneBackground == None:
					#~ self.zoneBackground = croppedGrayFrame
				#~ 
				#~ self.zoneBackground = np.add(np.multiply((1 - 0.1),self.zoneBackground), np.multiply(0.1,croppedGrayFrame))
				
				#~ diff = abs(np.subtract(croppedGrayFrame , self.zoneBackground))
				#~ self.mean = diff.mean()
				#~ self.variance = np.var(diff)
				#~ self.videoImageHandler.set_array(diff)
				#~ self.videoCanvas.draw()	
				#~ plt.clf()
				#~ plt.imshow(diff,self.color)
				
				#~ moments = cv2.moments(np.asarray(self.zoneArea,dtype=np.uint8))
				#~ variance1 = moments['mu02']
				#~ variance2 = moments['mu20']
				
				#~ cv2.drawContours(frame, [self.zoneArea], 0 , 255, 3)
				
		#~ thresholdedFrame  = cv2.inRange(diffFrame,np.array(10), np.array(50))
		#~ contours, hierarchy = cv2.findContours(thresholdedFrame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		#~ self.c = contours
		
		#~ if len(contours) > 0: 
			#~ areas = [cv2.contourArea(c) for c in contours]
			#~ index = np.argmax(areas)
			#~ contourMaxArea = contours[index]
			#~ 
			#~ self.findPeople(frame,contours[index])
			#~ 
			#~ self.contourMaxArea=cv2.contourArea(contourMaxArea)
			#~ cv2.drawContours(frame, [contourMaxArea], 0 , (0,0,0), 3)
			#~ self.countourImageHandler.set_array(frame)
			#~ self.countourCanvas.draw()
			#~ 
			#~ 
			#~ 
			#~ # This area saves the event. This needs to be added as a different thread and rewrite the code in order to catch 
			#~ # continuous events that differentiates as different events.
			#~ if max(areas) >= (self.frameArea/4):
				#~ self.count += 1
				#~ if self.count > 20:
					#~ self.eventLabel["text"] = "Events:-" + str(self.count)
					#~ self.bufferImages.append(frame)
					#~ self.currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			#~ else :
				#~ if self.bufferImages != []:
					#~ fourcc = cv2.cv.CV_FOURCC(*'PIM1')
					#~ videowriter = cv2.VideoWriter(str(self.currentTime)+'.mpeg',fourcc, 25, (640,480))
					#~ self.eventSave(self.bufferImages,videowriter)
					#~ self.bufferImages = []
					#~ del(videowriter)
		#~ print "ThresholdTime----:-",time.time() - tic							
	
	#~ def thresholdFrames(self,differenceFrame):
		#~ frame1 = differenceFrame > 30
		
if __name__ == "__main__":
	root = Tk()
	config = open('config.txt','r')
	for line in config:
			camUrl = line.split()
			if camUrl[1] == 'cam1':
				camUrl = camUrl[0]
				h= Motion(root,camUrl)
				h.cap.release()
				h.cap.open(camUrl)

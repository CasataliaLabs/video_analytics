#Date:- 18-Sep-2014
#Author - Sreeja S N
# Description :- Added the code to stream from bullet cam using urllib function 

# Note:- Please do not use this code as it is seems to be slow

import cv2
from repeated_timer_video_plot import RepeatedTimer
from Tkinter import *
import pylab
import numpy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
import urllib
#================================Functions==================================================
def video():

    global Gray_1 
    Gray_2 = convertToFrame(stream)
    axis.imshow(Gray_2)
    canvas.show()

    Gray_2 = cv2.cvtColor(Gray_2, cv2.COLOR_BGR2GRAY)

    Difference = abs(Gray_2 - Gray_1)
    Mean_value = numpy.mean(Difference)
    print Mean_value
    data = {'1':{'Mean Value': '{0:.3f}'.format(Mean_value)}}
    table.redrawTable()
    model.importDict(data)

    Gray_1 = Gray_2
    Values.append(Mean_value)
    Values.remove(Values[0])
    Plot[0].set_data(X_Axis, pylab.array(Values))
    canvas2.show()

    #if cv2.waitKey(1) & 0xFF == ord('q'):
     #   exit()


def video_start():
    t.start()

def video_stop():
    #cap.release()
    t.stop()

def convertToFrame(stream):
	global bytes	
	i = ''
	while True:
		bytes+=stream.read(1024)
		a = bytes.find('\xff\xd8')
    		b = bytes.find('\xff\xd9')
		if a!=-1 and b!=-1  :
        	     jpg = bytes[a:b+2]
		     bytes= bytes[b+2:]
        	     i = cv2.imdecode(numpy.fromstring(jpg, dtype=numpy.uint8),cv2.CV_LOAD_IMAGE_COLOR)
		     #i = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY) 
		     break
       		     if cv2.waitKey(1)==27:
                	exit(0)
	return i

#================================Functions==================================================

#================================Main Program===============================================
stream=urllib.urlopen('http://192.168.1.104/video.cgi')
bytes =''
#Gray_1 = convertToFrame(stream) 
Gray_1 = cv2.cvtColor(convertToFrame(stream), cv2.COLOR_BGR2GRAY)
t = RepeatedTimer(0,video)
Values = [0 for x in range(100)]
#===========================================================================================

#=================================GUI Section=============================================
root = Tk()
root.geometry('1000x700')

f = Figure(figsize=(4,4), dpi=50)
axis = f.add_subplot(111)
canvas = FigureCanvasTkAgg(f, master=root)
canvas.get_tk_widget().place(x=10,y=30)
frame2 = Frame(root)
frame2.place(x=20,y=300)
X_Axis = pylab.arange(0, 100, 1)
plotFigure = Figure(figsize=(4,4),dpi=50)
axis2 = plotFigure.add_subplot(111)
axis2.grid(True)
axis2.set_title("Mean value per Frame")
axis2.axis([0, 100, 0, 255])
Plot = axis2.plot(X_Axis, [0]*100, 'o-', color='r', markersize=6)

model = TableModel()
table = TableCanvas(frame2,model,height = 100,width=300)
model = table.model
table.createTableFrame()

canvas2 = FigureCanvasTkAgg(plotFigure, master=root)
canvas2.get_tk_widget().place(x=500,y=30)

b1 = Button(root,text="Start", bg='white', command=video_start).place(x=50,y=600)
b2 = Button(root,text="Stop", bg='white', command=video_stop).place(x=400,y=600)
root.mainloop()
#===========================================================================================

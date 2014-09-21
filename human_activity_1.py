#Date  :- 19-Sep-2014 
#Author:- Sreeja S N
#Description :- GUI of human activity analysis first stage.
#==============================================================================================================================
#Date  :- 20-Sep-2014
#Author:- Sreeja S N
#Description:- Compute new background frame using the current frame and previous background frame
#	       Show the current frame , background frame and the difference of the current frame and calculated background frame
#	       Used laptob cam for current being . Not able to stream from IP camera. Some issue showing with av_format_network_init() 

#================================================================================================================================

from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from repeated_timer_video_plot import RepeatedTimer
import cv2
import numpy as np
import matplotlib.pyplot as plt

#==============================================Functions========================================================================

def videoDisplay():
    global bck_frame
    ret, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    a1.imshow(gray_frame,color)
    c1.draw()
    
    if bck_frame == None:
	bck_frame = gray_frame

    diff_frame = abs(gray_frame-bck_frame)
    bck_frame = setBackGroundFrame(gray_frame,bck_frame)
    a2.imshow(diff_frame,color)
    c2.draw()

def setBackGroundFrame(gray_frame,bck_frame):
    a3.imshow(bck_frame,color)
    c3.draw()
    coefficient = float(e1.get())
    bck_gnd1 = np.add(np.multiply((1-coefficient),bck_frame), np.multiply(coefficient,gray_frame))
    return bck_gnd1

def videoStart():
    if not t.isRunning():
       t.start()    

def videoStop():
    if t.isRunning():
	t.stop()

#===================================Main Program========================================================
bck_frame = None
cap = cv2.VideoCapture()
#cap.open("http://admin:@192.168.1.105/snapshot.cgi?.mjpeg")
cap.open(0)
color = plt.get_cmap('gray')
t=RepeatedTimer(1,videoDisplay)
#================================================GUI Section====================================

master = Tk()
frame = Frame()
frame.grid()

f1 = plt.figure(figsize=(4,4), dpi=80)
a1 = f1.add_subplot(111)
a1.set_title('xn - Video')
a1.set_axis_off()
c1 = FigureCanvasTkAgg(f1, master=master)
c1.get_tk_widget().grid(row=0,columnspan=2)

f2 = plt.figure(figsize=(4,4),dpi = 80)
a2 = f2.add_subplot(111)
a2.set_title('xn-yn')
a2.set_axis_off()
c2 = FigureCanvasTkAgg(f2,master=master)
c2.get_tk_widget().grid(row=0,column=2,columnspan=3,pady=10)

lb1 = Label(master,text = 'Coefficient')
lb1.grid(row=3,sticky=S+W)

e1 = Entry(master,width=32)
e1.grid(row=3,column=1,sticky=S+W,columnspan=1)

b1 = Button(text='Calculate',bg='light blue' , command = videoStart).grid(row=4,column=1,sticky=N+W)
b2 = Button(text='Stop',bg='light blue' , command = videoStop,width=5).grid(row=4,column=1,sticky=N+E)

f3= plt.figure(figsize=(4,4),dpi = 80)
a3 = f3.add_subplot(111)
a3.set_title('yn - Background')
a3.set_axis_off()
c3 = FigureCanvasTkAgg(f3,master=master)
c3.get_tk_widget().grid(row=1,rowspan = 6,column=2,columnspan=3,pady=10,padx=10)
master.mainloop()
#===================================================================================================





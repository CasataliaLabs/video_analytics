from Tkinter import *
from matplotlib.pyplot import figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#~ import matplotlib.pyplot as plt
#~ plt.ion()

class HumanActivityInterface(object):

	def __init__(self,master):
		self.myParent = master
		
		width=self.myParent.winfo_screenwidth()
		height=self.myParent.winfo_screenheight()
		self.myParent.geometry(("%dx%d")%(width,height))
			
		self.myParent.title("Video Analysis")
		self.myContainer = Frame(master)
		self.myContainer.grid()
		
		self.coefficientLabel = Label(self.myContainer,text = 'Coefficient',takefocus=0)
		self.coefficientLabel.grid(row=1,sticky=S+W,padx=10,pady=20)
		
		
		self.coefficientEntry = Entry(self.myContainer,width=32)
		self.coefficientEntry.grid(row=1,column=1,sticky=S+W,padx=10,pady=20)
		
		self.buttonCalculate = Button(self.myContainer,bg='light blue')
		self.buttonCalculate["text"] = "Calculate"
		self.buttonCalculate.grid(row=1,column=2,sticky=S+W,padx=10,pady=20)
		self.buttonCalculate.bind("<Key>",self.videoStart)
		
		self.buttonTrain = Button(self.myContainer,text='Train',bg='light blue' ,width=5)
		self.buttonTrain.grid(row=17,column = 0,sticky=S+E)
		
		
		self.buttonStop = Button(self.myContainer,text='Stop',bg='light blue' ,width=5)
		self.buttonStop.grid(row=17,column=3,sticky=N+W,pady=10)
		self.buttonStop.bind("<Key>",self.videoStop)
		
		self.buttonExit = Button(self.myContainer,text='Exit',bg='light blue' ,width=5,command=self.exitForm)
		self.buttonExit.grid(row=17,column=6,sticky=N+E,pady=10)
		
		self.countourFig= figure(figsize=(4,4),dpi = 130)
		self.countourAxis = self.countourFig.add_subplot(111)
		self.countourAxis.set_title('Event detection')
		self.countourAxis.set_axis_off()
		self.countourCanvas = FigureCanvasTkAgg(self.countourFig,master=self.myContainer)
		self.countourCanvas.get_tk_widget().grid(row=2,column=3,columnspan=4,rowspan=15)
		
		self.videoFig = figure(figsize=(4,4), dpi=80)
		self.videoAxis = self.videoFig.add_subplot(111)
		self.videoAxis.set_title('Video')
		self.videoAxis.set_axis_off()
		self.videoCanvas = FigureCanvasTkAgg(self.videoFig, master=self.myContainer)
		self.videoCanvas.get_tk_widget().grid(row=2,columnspan=2,rowspan=4)
		
		self.timer = self.videoCanvas.new_timer(interval=10)
		
		#~ self.cFrame = Frame(self.myContainer)
		#~ self.cFrame.grid(row=8,columnspan=2,rowspan=3)
		
		self.dataFig = figure(figsize=(4,3))
		self.dataAxis=self.dataFig.gca()
		self.dataAxis.set_axis_off()
		self.dataCanvas = FigureCanvasTkAgg(self.dataFig, master=self.myContainer)
		self.dataCanvas.get_tk_widget().grid(row=8,columnspan=2,rowspan=3)
		
		#~ self.vscrollbar=Scrollbar(self.cFrame,orient=VERTICAL)
		#~ self.vscrollbar.grid(sticky=E)
		

		self.eventLabel = Label(self.myContainer,text = 'Events:-')
		self.eventLabel.grid(row=1,column=6,columnspan=3)
		
	
	def videoStart(self,event):
		if  (str(event.keysym) == 'Return') | (str(event.keysym) == 'space'):
			self.timer.start()
	
	def videoStop(self,event):
		if  (str(event.keysym) == 'Return') | (str(event.keysym) == 'space'):
			self.timer.stop()	
		
	def exitForm(self):
		self.cap.release()
		self.myParent.destroy()	
		
#~ root = Tk()
#~ h = HumanActivityInterface(root)
#~ root.mainloop()

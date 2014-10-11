from Tkinter import *
from matplotlib.pyplot import figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class HumanActivityInterface(object):

	def __init__(self,master):
		self.myParent = master
		
		width=self.myParent.winfo_screenwidth()
		height=self.myParent.winfo_screenheight()
		self.myParent.geometry(("%dx%d")%(width,height))
		
		self.myParent.title("Video Analysis")
		self.myContainer = Frame(master,background="white")
		self.myContainer.grid()
		
		self.videoFig = figure(figsize=(4,4), dpi=80)
		self.videoAxis = self.videoFig.add_subplot(111)
		self.videoAxis.set_title('xn - Video')
		self.videoAxis.set_axis_off()
		self.videoCanvas = FigureCanvasTkAgg(self.videoFig, master=self.myContainer)
		self.videoCanvas.get_tk_widget().grid(row=0,columnspan=2)
		self.videoCanvas.show()
		
		self.timer = self.videoCanvas.new_timer(interval=10)
		
		self.differenceFig = figure(figsize=(4,4),dpi = 80)
		self.differenceAxis = self.differenceFig.add_subplot(111)
		self.differenceAxis.set_title('xn-yn')
		self.differenceAxis.set_axis_off()
		self.differenceCanvas = FigureCanvasTkAgg(self.differenceFig,master=self.myContainer)
		self.differenceCanvas.get_tk_widget().grid(row=0,column=2,columnspan=3,pady=10)
		self.differenceCanvas.show()
		
		self.coefficientLabel = Label(self.myContainer,text = 'Coefficient')
		self.coefficientLabel.grid(row=3,sticky=S+W)
		
		self.coefficientEntry = Entry(self.myContainer,width=32)
		self.coefficientEntry.grid(row=3,column=1,sticky=S+W,columnspan=1)
		
		self.buttonCalculate = Button(self.myContainer,bg='light blue')
		self.buttonCalculate["text"] = "Calculate"
		self.buttonCalculate.grid(row=4,column=1,sticky=N+W)
		self.buttonCalculate.bind("<Button-1>",self.videoStart)
		
		self.buttonStop = Button(self.myContainer,text='Stop',bg='light blue' ,width=5)
		self.buttonStop.grid(row=4,column=1,sticky=N+E)
		self.buttonStop.bind("<Button-1>",self.videoStop)
				
		self.backgroundFig= figure(figsize=(4,4),dpi = 80)
		self.backgroundAxis = self.backgroundFig.add_subplot(111)
		self.backgroundAxis.set_title('yn - Background')
		self.backgroundAxis.set_axis_off()
		self.backgroundCanvas = FigureCanvasTkAgg(self.backgroundFig,master=self.myContainer)
		self.backgroundCanvas.get_tk_widget().grid(row=1,rowspan = 6,column=2,columnspan=3,pady=10)
		self.backgroundCanvas.show()
		
		self.countourFig= figure(figsize=(4,4),dpi = 80)
		self.countourAxis = self.countourFig.add_subplot(111)
		self.countourAxis.set_title('Event detection')
		self.countourAxis.set_axis_off()
		self.countourCanvas = FigureCanvasTkAgg(self.countourFig,master=self.myContainer)
		self.countourCanvas.get_tk_widget().grid(row=0,column=6,columnspan=3,pady=10)
		self.countourCanvas.show()
		
		self.eventLabel = Label(self.myContainer,text = 'Events:-')
		self.eventLabel.grid(row=1,column=6,columnspan=3)
		
	
	def videoStart(self,event):
		self.timer.start()
		
	def videoStop(self,event):
		self.timer.stop()

#root = Tk()
#h = HumanActivityInterface(root)
#root.mainloop()

from Tkinter import *
from PIL import ImageTk, Image
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
		
		#~ self.coefficientLabel = Label(self.myContainer,text = 'Coefficient',takefocus=0)
		#~ self.coefficientLabel.grid(row=1,sticky=S+W,padx=10,pady=20)
		
		
		#~ self.coefficientEntry = Entry(self.myContainer,width=32)
		#~ self.coefficientEntry.grid(row=1,column=1,sticky=S+W,padx=10,pady=20)
		self.original = Image.open("logo.jpeg")
		#~ self.resized = self.original.resize((300, 120),Image.ANTIALIAS)
		
		self.logo = ImageTk.PhotoImage(self.original)
		self.logoLabel = Label(self.myContainer,image=self.logo)
		#~ self.logoLabel.photo=self.logo
		self.logoLabel.grid(row=0,column=0,columnspan=2,sticky=N+S+E+W,pady=5,padx=10)
		
		
		
		self.buttonCalculate = Button(self.myContainer,bg='light blue',width=7)
		self.buttonCalculate["text"] = "Calculate"
		self.buttonCalculate.grid(row=1,column=0,sticky=N+W,padx=10,pady=20)
		self.buttonCalculate.bind("<Key>",self.videoStart)
		
		
		self.buttonStop = Button(self.myContainer,text='Stop',bg='light blue' ,width=7)
		self.buttonStop.grid(row=2,column=0,sticky=N+W,padx=10,pady=20)
		self.buttonStop.bind("<Key>",self.videoStop)
		
		self.buttonExit = Button(self.myContainer,text='Exit',bg='light blue' ,width=7,command=self.exitForm)
		self.buttonExit.grid(row=3,column=0,sticky=N+W,padx=10,pady=20)
		
		self.buttonTrain = Button(self.myContainer,text='Train',bg='light blue' ,width=7)
		self.buttonTrain.grid(row=4,column = 0,sticky=N+W,padx=10,pady=20)
		
		self.countourFig= figure(figsize=(4,4),dpi = 80)
		self.countourAxis = self.countourFig.add_subplot(111)
		self.countourAxis.set_title('Video')
		self.countourAxis.set_axis_off()
		self.countourCanvas = FigureCanvasTkAgg(self.countourFig,master=self.myContainer)
		self.countourCanvas.get_tk_widget().grid(row=0,column=12,rowspan=5)
		
		self.videoFig = figure(figsize=(6,5), dpi=140)
		self.videoAxis = self.videoFig.add_subplot(111)
		self.videoAxis.set_title('Human Detection')
		self.videoAxis.set_axis_off()
		self.videoCanvas = FigureCanvasTkAgg(self.videoFig, master=self.myContainer)
		self.videoCanvas.get_tk_widget().grid(row=0,column=2,columnspan=10,rowspan=10,pady=15)
		
		self.timer = self.videoCanvas.new_timer(interval=10)
		
		#~ self.cFrame = Frame(self.myContainer)
		#~ self.cFrame.grid(row=8,columnspan=2,rowspan=3)
		
		#~ self.dataFig = figure(figsize=(4,3))
		#~ self.dataAxis=self.dataFig.gca()
		#~ self.dataAxis.set_axis_off()
		#~ self.dataCanvas = FigureCanvasTkAgg(self.dataFig, master=self.myContainer)
		#~ self.dataCanvas.get_tk_widget().grid(row=8,columnspan=2,rowspan=3)
		
		#~ self.vscrollbar=Scrollbar(self.cFrame,orient=VERTICAL)
		#~ self.vscrollbar.grid(sticky=E)
		

		#~ self.eventLabel = Label(self.myContainer,text = 'Events:-')
		#~ self.eventLabel.grid(row=1,column=6,columnspan=3)
		
	
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

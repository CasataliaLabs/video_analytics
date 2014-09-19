#Date :- 19-Sep-2014 
#Author - Sreeja S N
#Description :- GUI of human activity analysis first stage.

from Tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

master = Tk()
frame = Frame()
#frame.rowconfigure( 6, weight = 1 )
#frame.columnconfigure( 2, pad=20 )
frame.grid()


f1 = Figure(figsize=(4,4), dpi=50)
#axis = f1.add_subplot(111)
canvas = FigureCanvasTkAgg(f1, master=master)
canvas.get_tk_widget().grid(row=0,columnspan=2,pady=2)

f2 = Figure(figsize=(4,4),dpi = 50)
canvas = FigureCanvasTkAgg(f2,master=master)
canvas.get_tk_widget().grid(row=0,column=2,columnspan=2,padx=8)

lb1 = Label(master,text = 'Coefficient')
lb1.grid(row=3,sticky=W+S)
e1 = Entry(master)
e1.grid(row=3,column=1,sticky=W+S)

f3= Figure(figsize=(4,4),dpi = 50)
canvas = FigureCanvasTkAgg(f3,master=master)
canvas.get_tk_widget().grid(row=1,rowspan = 6,column=2,columnspan=2)

b1 = Button(text='Calculate',bg='light blue').grid(row=4,column=1,sticky=N+W,pady=2)
master.mainloop()


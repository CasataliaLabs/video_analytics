# Simple example of using general timer objects. This is used to update
# the time placed in the title of the figure.
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time
plt.ion()
#~ import cv2
#~ from repeated_timer import RepeatedTimer
#~ cap = cv2.VideoCapture(0)
#~ cap.open(0)
#~ ret, frame = cap.read()

def update_title(axes, hAx, x):
	tic = time.time()
	axes.set_title(datetime.now())
	y = np.random.randn(x.size)
	#~ ax.clear()
	#~ axes.plot(x, y)
	y = np.random.randn(10, 20)
	#~ axes.imshow(y)
	hAx.set_array(y)
	axes.figure.canvas.show()
	toc = time.time() - tic
	print (toc)
fig, ax = plt.subplots()
x = np.linspace(-3, 3)
y = np.random.randn(10, 20)
#~ hAx = ax.plot(x, x*x)
hAx = ax.imshow(y)


# Create a new timer object. Set the interval 500 milliseconds (1000 is default)
# and tell the timer what function should be called.
timer = fig.canvas.new_timer(interval=100)
timer.add_callback(update_title, ax, hAx, x)
timer.start()

#Or could start the timer on first figure draw
#def start_timer(evt):
#    timer.start()
#    fig.canvas.mpl_disconnect(drawid)
#drawid = fig.canvas.mpl_connect('draw_event', start_timer)

plt.show()

import base64
from datetime import datetime
import httplib
import io
import os
import time

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

import numpy as np
import matplotlib.pyplot as plt

#~ wdir = "workdir"
stream_url = '192.168.1.104'

username = 'admin'
password = 'admin'

class CameraAcquisitionHighSpeed():

	def __init__(self):
		self.stream_url = '192.168.1.104'
		self.username = 'admin'
		self.password = 'admin'
		h = httplib.HTTP(self.stream_url)
		h.putrequest('GET', '/video.cgi')
		h.putheader('Authorization', 'Basic %s' % base64.encodestring('%s:%s' % (self.username, self.password))[:-1])
		h.endheaders()
		errcode, errmsg, headers = h.getreply()
		self.stream_file = h.getfile()
		self.h = h

	def ReadFRameAsNp(self):
		source_name = self.stream_file.readline()    # '--ipcamera'
		content_type = self.stream_file.readline()    # 'Content-Type: image/jpeg'
		content_length = self.stream_file.readline()   # 'Content-Length: 19565'
		print 'confirm/adjust content (source?): ' + source_name
		print 'confirm/adjust content (type?): ' + content_type
		print 'confirm/adjust content (length?): ' + content_length
		# find the beginning of the jpeg data BEFORE pulling the jpeg framesize
		# there must be a more efficient way, but hopefully this is not too bad
		b1 = b2 = b''
		while True:
			b1 = self.stream_file.read(1)
			while b1 != chr(0xff):
				b1 = self.stream_file.read(1)
			b2 = self.stream_file.read(1)
			if b2 == chr(0xd8):
				break
		# pull the jpeg data
		framesize = int(content_length[16:])
		jpeg_stripped = b''.join((b1, b2, self.stream_file.read(framesize - 2)))
		# throw away the remaining stream data. Sorry I have no idea what it is
		junk_for_now = self.stream_file.readline()
		# convert directly to an Image instead of saving / reopening
		# thanks to SO: http://stackoverflow.com/a/12020860/377366
		image_as_file = io.BytesIO(jpeg_stripped)
		image_as_pil = Image.open(image_as_file)
		self.image_as_np = np.asarray(image_as_pil)
		
		return self.image_as_np
	

#~ if __name__ == '__main__':
    #~ main()

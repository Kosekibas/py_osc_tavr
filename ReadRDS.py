

# import struct

# fmt="<HI1s1sB" #два
# # байтовых символов 
# BLOCK_SIZE=struct.calcsize(fmt)
# #assert BLOCK_SIZE==8

# with open("C:/KOS/temp_log.rdf","rb") as f:
# 	tmpbuf = f.read()
    
# 	counter, time, text1, text2, state = struct.unpack_from(fmt, tmpbuf,9)
    
# 	#print(f"{counter}\t{time}\t{text1.decode('utf-8')}")
import time

# import numpy as np
# bufType=np.dtype(
# 	[
# 		('counter', 'i2'),
# 		('time', 'i4'),
# 		('text_1', 'S1'),
#         ('text_2', 'S1'),
#         ('state', 'i1')
# 	]
# )

# data = np.fromfile('C:/KOS/PyOsc/1.rdf', dtype=bufType,offset=30486)

# print(data)
# print(time.localtime(data[1]['time']))

import numpy as nposc
bufType=nposc.dtype(
	[
		('Ia1', 'i2'),
		('Ic1', 'i2'),
		('Ia2', 'i2'),
        ('Ic2', 'i2'),
        ('Iakt', 'i2'),
        ('Ickt', 'i2'),
		('Uab1', 'i2'),
		('Uab2', '<i2'),
              ('Dio', 'u4')
        ]
)

osc = nposc.fromfile('E:/KosPy/Samples/py_osc_tavr/Osc/2.rdf', dtype=bufType,count=1500,offset=34)




#График мультизонный
# https://nbviewer.jupyter.org/github/whitehorn/Scientific_graphics_in_python/blob/master/P2%20Chapter%207%20Subplots.ipynb
# https://pyprog.pro/mpl/mpl_main_components.html
import matplotlib.pyplot as plt

fig, axes = plt.subplots(nrows=32, ncols=1)

n = 1
for ax in axes.flat:
    
    ax.set(xticks=[], yticks=[])
    ax.set_ylim(ymin=-0.1,ymax=1.1)
    ax.set_xlim(xmin=0,xmax=1500)
    ax.text(-100, 0.5, 'DIO_' + str(n), color='red')
    ax.stem ( ~(osc['Dio'] >> n-1) & 1 , linefmt='C0-', markerfmt='C0-', basefmt='C0-') 
    
    n += 1
    
plt.show()

#save('pic_7_2_1', fmt='png')
#save('pic_7_2_1', fmt='pdf')


#!!

#plt.plot(osc['Dio'])
#print (dio)
#plt.plot(dio)
#plt.show()

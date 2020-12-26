

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
      
        ('osc29', 'u1'),
        ('osc30', 'u1'),
        ('osc31', 'u1'),
        ('osc32', 'u1')
        ]
)

osc = nposc.fromfile('E:/KosPy/Samples/py_osc_tavr/Osc/1.rdf', dtype=bufType,count=1000,offset=34)


import matplotlib.pyplot as plt

plt.plot(osc['osc32'])
plt.show()

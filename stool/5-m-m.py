import re
import matplotlib.pyplot as plt
import random
import numpy as np
import matplotlib as mpl
from pylab import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

file_path = "./0810-4.txt"
print("start.....")
log = open(file_path,"r")
#
pick_lines = []
smp_rst = []
smp_rst_show = []
one = 0
zero =0
delt = []
long_one =[]
long_one_cnt =0
long_zero = []
long_zero_cnt = 0

plt.figure(num=1,figsize=(12, 4))
ymajorLocator  = MultipleLocator(2)
ax = plt.gca()
plt.grid()
plt.xlim(-4,288)
plt.ylim(-35,17)
#plt.subplots_adjust(bottom = 0.1)

ax.xaxis.set_major_locator( MultipleLocator(10))
ax.xaxis.set_minor_locator( MultipleLocator(2) )

ax.yaxis.set_major_locator( MultipleLocator(5))
ax.yaxis.set_minor_locator( MultipleLocator(1) )

line_list = log.readlines()

#get all lines
for idx in range(len(line_list)):
    line = line_list[idx]
    pick_lines.append(line)

#get sample
for j in range(len(pick_lines)):
    x = pick_lines[j]
    for k in range(len(x)):
        if x[k].isdigit():
            smp_rst.append(int(x[k]))
            smp_rst_show.append(int(x[k]) + 13)

#expand for better show
for j in range(len(smp_rst_show)):
    if smp_rst_show[j] == 13:
        smp_rst_show[j] = smp_rst_show[j] - 1

#1-0 delt analyze
for i in range(len(smp_rst)):
    if(smp_rst[i] == 1):
        one = one +1
    if(smp_rst[i] == 0):
        zero = zero + 1
    delt.append((one-zero))
    #print("[1]=%d [0]=%d 0-1=%d" %(one,zero,one-zero))

#long one and long zero analyze
cnt_idx = 0
for k in range(0,len(smp_rst),1):
    if smp_rst[k] == 1:
        long_one_cnt = long_one_cnt +1
        long_one.append(0)
#do zero
        if(long_zero_cnt > 1):
            long_zero.append(long_zero_cnt)
        else:
            long_zero.append(0)
        long_zero_cnt = 0
    else:
        if(long_one_cnt > 1):
            long_one.append(long_one_cnt)
        else:
            long_one.append(0)
        long_one_cnt = 0
#do zero
        long_zero_cnt = long_zero_cnt + 1
        long_zero.append(0)
    

#print(long_one)       
#print (smp_rst)        
plt.plot(smp_rst_show,color='green',marker='.',label ='true')
plt.plot(delt,color='red',marker='.',label ='true')
plt.plot(long_one,color='darkblue',marker='.',label ='true')
plt.plot(long_zero,color='brown',marker='.',label ='true')

plt.show()
log.close()


            
print("end .....")

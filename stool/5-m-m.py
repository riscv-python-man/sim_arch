import re
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from pylab import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import random

file_path = "./1002-4.txt"
print("start.....")

normal_run = 1
window_size = 5

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


cnt_idx = 0

long_2_1 =0
long_3_1 =0
long_4_1=0
long_5_1 =0
long_6_1 =0
long_7_1 =0
long_8_1 =0
long_9_1 =0
long_10_1 =0
long_11_1 =0


long_2_0 =0
long_3_0 =0
long_4_0 =0
long_5_0 =0
long_6_0 =0
long_7_0 =0
long_8_0 =0
long_9_0 =0
long_10_0 =0
long_11_0 =0


plt.figure(num=1,figsize=(12, 4))
ymajorLocator  = MultipleLocator(2)
ax = plt.gca()
plt.grid()
plt.xlim(-4,294)
plt.ylim(-50,100)

ax.xaxis.set_major_locator(MultipleLocator(10))
ax.xaxis.set_minor_locator(MultipleLocator(1) )
ax.yaxis.set_major_locator(MultipleLocator(5))
ax.yaxis.set_minor_locator(MultipleLocator(1) )

log = open(file_path,"r")
line_list = log.readlines()

#get all lines
for idx in range(len(line_list)):
    line = line_list[idx]
    pick_lines.append(line)

if normal_run == 1:
#get sample
    for j in range(len(pick_lines)):
        x = pick_lines[j]
        for k in range(len(x)):
            if x[k].isdigit():
                smp_rst.append(int(x[k]))
                smp_rst_show.append(int(x[k]) - 30)

#training  sequnce
else:
    for x in range(0,288,1):
        smp_rst.append(random.randint(0,1))
        smp_rst_show.append(smp_rst[x] -30) 
            

for i in range(0,window_size + 1,1):
    smp_rst.append(0)

#expand for better show
for j in range(len(smp_rst_show)):
    if smp_rst_show[j] == -30:
        smp_rst_show[j] = smp_rst_show[j] - 4

#1-0 delt analyze
for i in range(len(smp_rst)):
    if(smp_rst[i] == 1):
        one = one +1
    if(smp_rst[i] == 0):
        zero = zero + 1
    delt.append((one-zero) - 5)
    #print("[1]=%d [0]=%d 0-1=%d" %(one,zero,one-zero))
win_1 = 0
win_0 = 0
win_1_list = []
win_0_list = []
lost_1 = 0
lost_0 = 0
total_0 = 0
total_1 = 0


#long one and long zero analyze
for k in range(0,len(smp_rst) - window_size,1):
    x = k
    long_2_1 =0
    long_3_1 =0
    long_4_1=0
    long_5_1 =0
    long_6_1 =0
    long_7_1 =0
    long_8_1 =0
    long_9_1 =0
    long_10_1 =0
    long_11_1 =0
    
    long_2_0 =0
    long_3_0 =0
    long_4_0 =0
    long_5_0 =0
    long_6_0 =0
    long_7_0 =0
    long_8_0 =0
    long_9_0 =0
    long_10_0 =0
    long_11_0 =0
    long_one_cnt = 0
    long_zero_cnt = 0
    lost_0 = 0
    lost_1 = 0
    win_0 = 0
    win_1 = 0

    
    for x in range(k, window_size + k +1  ,1):
        if smp_rst[x] == 1: #do one
            long_one_cnt +=1
            long_one.append(0)
            lost_0 += 1

            if(long_zero_cnt == 1):
                win_0 +=2
            if long_zero_cnt == 2:
                long_2_0 +=1
                win_0 +=4
            if long_zero_cnt == 3:
                long_3_0 +=1
                win_0 +=8
            if long_zero_cnt == 4:
                long_4_0 +=1
                win_0 +=16
            if long_zero_cnt == 5:
                long_5_0 +=1
                win_0 +=32
            if long_zero_cnt == 6:
                long_6_0 +=1
                win_0 +=64
            if long_zero_cnt == 7:
                long_7_0 +=1
                win_0 +=128
            if long_zero_cnt == 8:
                long_8_0 +=1
                win_0 +=256
            if long_zero_cnt == 9:
                long_9_0 +=1
                win_0 += 512
            if long_zero_cnt == 10:
                long_10_0 +=1
                win_0 += 1024
            if long_zero_cnt == 11:
                long_11_0 +=1
                win_0 += 2048
            
            if(long_zero_cnt > 1):
                long_zero.append(long_zero_cnt)
            else:
                long_zero.append(0)
            long_zero_cnt = 0
        
        else:#do zero
            long_zero_cnt += 1
            long_zero.append(0)
            lost_1 +=1

            if long_one_cnt == 1:
                win_1 += 2                 
            if long_one_cnt == 2:
                long_2_1 +=1
                win_1 += 4
            if long_one_cnt == 3:
                long_3_1 +=1
                win_1 += 8
            if long_one_cnt == 4:
                long_4_1 +=1
                win_1 += 16
            if long_one_cnt == 5:
                long_5_1 +=1
                win_1 +=32
            if long_one_cnt == 6:
                long_6_1 +=1
                win_1 += 64
            if long_one_cnt == 7:
                long_7_1 +=1
                win_1 += 128
            if long_one_cnt == 8:
                long_8_1 +=1
                win_1 += 256
            if long_one_cnt == 9:
                long_9_1 +=1
                win_1 += 512
            if long_one_cnt == 10:
                long_10_1 +=1
                win_1 += 1024
            if long_one_cnt == 11:
                long_11_1 +=1
                win_1 += 2048

            if(long_one_cnt > 1):
                long_one.append(long_one_cnt)
            else:
                long_one.append(0)
            long_one_cnt = 0
            
            
    win_1_list.append(win_1-lost_1-1) 
    win_0_list.append(win_0-lost_0-1)
   
    
#print(long_one)       
#print (smp_rst)
#print("totoal long 1 %d totoal long 0 %d" % (, ))        
'''
long_x0 = [long_2_0,0,0,0,0,0,0,0,0,0,0,0,0,long_3_0,0,0,0,0,0,0,0,0,0,0,0,0,long_4_0,0,0,0,0,0,0,0,0,0,0,0,0,long_5_0,0,0,0,0,0,0,0,0,0,0,0,0,
           long_6_0,0,0,0,0,0,0,0,0,0,0,0,0,long_7_0,0,0,0,0,0,0,0,0,0,0,0,0,long_8_0,0,0,0,0,0,0,0,0,0,0,0,0,long_9_0,0,0,0,0,0,0,0,0,0,0,0,0,
           long_10_0,0,0,0,0,0,0,0,0,0,0,0,0,long_11_0,0,0,0,0,0,0,0,0,0,0,0,0]
long_x1 = [long_2_1,0,0,0,0,0,0,0,0,0,0,0,0,long_3_1,0,0,0,0,0,0,0,0,0,0,0,0,long_4_1,0,0,0,0,0,0,0,0,0,0,0,0,long_5_1,0,0,0,0,0,0,0,0,0,0,0,0,
           long_6_1,0,0,0,0,0,0,0,0,0,0,0,0,long_7_1,0,0,0,0,0,0,0,0,0,0,0,0,long_8_1,0,0,0,0,0,0,0,0,0,0,0,0,long_9_1,0,0,0,0,0,0,0,0,0,0,0,0,
           long_10_1,0,0,0,0,0,0,0,0,0,0,0,0,long_11_1,0,0,0,0,0,0,0,0,0,0,0,0]

for i in range(len(long_x0)):
    long_x0[i] -= 40
    long_x1[i] -= 20           
'''
longx_idx = [2,3,4,5,6,7,8,9,10,11]
long_x0 = [long_2_0,long_3_0,long_4_0,long_5_0,long_6_0,long_7_0,long_8_0,long_9_0,long_10_0,long_11_0]
long_x1 = [long_2_1,long_3_1,long_4_1,long_5_1,long_6_1,long_7_1,long_8_1,long_9_1,long_10_1,long_11_1]

if normal_run == 1:
    print("---win in file",file_path)
else:
    print("---win in self test\n")

print("cnt",longx_idx)
print("_x1",long_x1)
print("_x0",long_x0)

print("window_size,max_1, max_0, min_1, min_0\n",(window_size,max(win_1_list),max(win_0_list),min(win_1_list),min(win_0_list)))

#print("win_1",win_1 - total_0)
#print("win_0",win_0 - total_1)

print("win_1",win_1_list)
print("win_0",win_0_list)


plt.plot(smp_rst_show,color='green',marker='.',label ='smp')
plt.plot(delt,color='red',marker='.',label ='delt(1-0):%d'%(one-zero))

plt.plot(win_1_list,color='brown',marker='.',label ='win_1')
plt.plot(win_0_list,color='darkblue',marker='.',label ='win_0')

#plt.plot(long_zero,color='brown',marker='.',label ='L0=%d [0]=%d' % (,zero))
#plt.plot(long_one,color='darkblue',marker='.',linestyle=':',label ='L1=%d [1]=%d' % (,one))
#plt.plot(long_x0,color='black',marker='.',linestyle=':',label ='L0 dist')
#plt.plot(long_x1,color='cyan',marker='.',label ='L1 dist')

plt.legend(loc='best', fontsize=8)
plt.show()

log.close()
 
print("end .....")

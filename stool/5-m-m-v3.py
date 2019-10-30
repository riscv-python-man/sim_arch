import re
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from pylab import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import random

file_path = "./0812-4.txt"
print("start.....")

normal_run = 1

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
total_long_1 = 0
total_long_0 = 0
single_1 = 0
single_0 =0
jump_10_cnt = 0
jump_01_cnt = 0

long_ref_array = [i+1 for i in range(11)]
long_zero_array = [0  for i in range(11)]
long_one_array = [0 for i in range(11)]
#print (long_zero_array)
#print (long_one_array)

plt.figure(num=1,figsize=(12, 4))
ymajorLocator  = MultipleLocator(2)
ax = plt.gca()
plt.grid()
plt.xlim(-4,294)
plt.ylim(-40,20)

ax.xaxis.set_major_locator(MultipleLocator(10))
ax.xaxis.set_minor_locator(MultipleLocator(1) )
ax.yaxis.set_major_locator(MultipleLocator(5))
ax.yaxis.set_minor_locator(MultipleLocator(1) )

log = open(file_path,"r")
line_list = log.readlines()

#get all lines: strip a line to avoid space line
for i, v in enumerate(line_list):
    if not len(line_list[i].strip()): 
        continue
    pick_lines.append(line_list[i])


if normal_run == 1:
#get sample
    for j in range(len(pick_lines)):
        x = pick_lines[j]
        for k in range(len(x)):
            if x[k].isdigit():
                smp_rst.append(int(x[k]))
                smp_rst_show.append(int(x[k]))

#training  sequnce
else:
    for x in range(0,28800,1):
        smp_rst.append(random.randint(0,1))
        smp_rst_show.append(smp_rst[x]) 
            

#expand for better show
for j in range(len(smp_rst_show)):
    if smp_rst_show[j] == 0:
        smp_rst_show[j] -= 5

#1-0 delt analyze
for i in range(len(smp_rst)):
    if(smp_rst[i] == 1):
        one += 1
    if(smp_rst[i] == 0):
        zero += 1
    delt.append(one - zero)
    #print("[1]=%d [0]=%d 0-1=%d" %(one,zero,one-zero))

last_0 = 0
last_1 = 0
#long one and long zero analyze
for k in range(0,len(smp_rst),1):
    if smp_rst[k] == 1: # when seq ==1 
        if last_0 == 0:
            jump_01_cnt +=1
            last_0 = 1

        last_1 = 1
        long_one_cnt += 1
        long_one.append(0)

        if(long_zero_cnt >= 1):
            long_zero.append(long_zero_cnt)
            total_long_0 += 1
        else:
            long_zero.append(0)

        for m,v in enumerate(long_ref_array):
            if long_zero_cnt == long_ref_array[m]:
                long_zero_array[m] +=1

        if long_zero_cnt == 1:
            single_0 +=1
        long_zero_cnt = 0
    else:             #when seq == 0
        if last_1 == 1:
            jump_10_cnt += 1
            last_1 = 0
            
        last_0 = 0
        if(long_one_cnt >= 1):
            long_one.append(long_one_cnt)
            total_long_1 += 1
        else:
            long_one.append(0)

        for n,u in enumerate(long_ref_array):
            if long_one_cnt == long_ref_array[n]:
                long_one_array[n] +=1

        if long_one_cnt == 1:
            single_1 += 1
        long_one_cnt = 0    
#do zero
        long_zero_cnt +=1
        long_zero.append(0)
    
#print(long_one)       
#print (smp_rst)
#print("totoal long 1 %d totoal long 0 %d" % (total_long_1, total_long_0))        



for i, val in enumerate(long_ref_array):
    print("%2d: zero %2d one %2d "%(long_ref_array[i],long_zero_array[i],long_one_array[i]))
print("seq:  L0=%d L1=%d S0=%d S1=%d,J10=%d J01=%d" %(total_long_0,total_long_1, single_0, single_1, jump_10_cnt, jump_01_cnt))


for i,v in enumerate(long_zero):
    long_zero[i] += 10

for i,v in enumerate(long_one):
    long_one[i] += 5

for i,v in enumerate(delt):
    delt[i] -= 5

for i,v in enumerate(smp_rst_show):
    smp_rst_show[i] -= 20

    
plt.plot(smp_rst_show,color='green',marker='.',label ='origin')
plt.plot(delt,color='red',marker='.',label ='delt : 0 -1  = %d'%(zero - one))

plt.plot(long_zero,color='brown',marker='.',label ='L0=%d [0]=%d\n[2]=%d [3]=%d [4]=%d [5]=%d [6]=%d [7]=%d [8]=%d [9]=%d [10]=%d [11]=%d'\
         % (total_long_0-long_zero_array[0],zero,long_zero_array[1],long_zero_array[2],long_zero_array[3],long_zero_array[4],long_zero_array[5],\
            long_zero_array[6],long_zero_array[7],long_zero_array[8],long_zero_array[9],long_zero_array[10]))

plt.plot(long_one,color='darkblue',marker='.',linestyle=':',label ='L1=%d [1]=%d\n[2]=%d [3]=%d [4]=%d [5]=%d [6]=%d [7]=%d [8]=%d [9]=%d [10]=%d [11]=%d'\
         %(total_long_1 - long_one_array[0],one, long_one_array[1],long_one_array[2],long_one_array[3],long_one_array[4],long_one_array[5],long_one_array[6],\
           long_one_array[7],long_one_array[8],long_one_array[9],long_one_array[10]))


plt.legend(loc='best', fontsize=8)
plt.show()

log.close()
 
print("end .....")

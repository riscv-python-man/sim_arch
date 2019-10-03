import re
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from pylab import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import random

file_path_4 = "./0808-4.txt"
file_path_3 = "./0809-4.txt"
file_path_2 = "./0810-4.txt"
file_path_1 = "./0811-4.txt"
file_path_0 = "./0812-4.txt"

print("start.....")

normal_run = 1

pick_lines_4 = []
pick_lines_3 = []
pick_lines_2 = []
pick_lines_1 = []
pick_lines_0 = []

sample_list_4 = []
sample_list_3 = []
sample_list_2 = []
sample_list_1 = []
sample_list_0 = []

sample_list_4_show = []
sample_list_3_show = []
sample_list_2_show = []
sample_list_1_show = []
sample_list_0_show = []


delt_4 = []
delt_3 = []
delt_2 = []
delt_1 = []
delt_0 = []

plt.figure(num=1,figsize=(12, 4))
ymajorLocator  = MultipleLocator(2)
ax = plt.gca()
plt.grid()
plt.xlim(-4,294)
plt.ylim(-50,50)

ax.xaxis.set_major_locator(MultipleLocator(10))
ax.xaxis.set_minor_locator(MultipleLocator(1) )
ax.yaxis.set_major_locator(MultipleLocator(5))
ax.yaxis.set_minor_locator(MultipleLocator(1) )

log_4 = open(file_path_4,"r")
log_3 = open(file_path_3,"r")
log_2 = open(file_path_2,"r")
log_1 = open(file_path_1,"r")
log_0 = open(file_path_0,"r")



line_list_4 = log_4.readlines()
line_list_3 = log_3.readlines()
line_list_2 = log_2.readlines()
line_list_1 = log_1.readlines()
line_list_0 = log_0.readlines()

one = 0
zero =0

#get all lines
for idx in range(len(line_list_4)):
    line = line_list_4[idx]
    pick_lines_4.append(line)

if normal_run == 1:
#get sample
    for j in range(len(pick_lines_4)):
        x = pick_lines_4[j]
        for k in range(len(x)):
            if x[k].isdigit():
                sample_list_4.append(int(x[k]))
                sample_list_4_show.append(int(x[k]) - 30)

#training  sequnce
else:
    for x in range(0,288,1):
        sample_list_4.append(random.randint(0,1))
        sample_list_4_show.append(sample_list_4[x] -30) 
            

#expand for better show
for j in range(len(sample_list_4_show)):
    if sample_list_4_show[j] == -30:
        sample_list_4_show[j] = sample_list_4_show[j] - 4

#1-0 delt_4 analyze
for i in range(len(sample_list_4)):
    if(sample_list_4[i] == 1):
        one = one +1
    if(sample_list_4[i] == 0):
        zero = zero + 1
    delt_4.append((one-zero) - 5)
    #print("[1]=%d [0]=%d 0-1=%d" %(one,zero,one-zero))

#get all lines
for idx in range(len(line_list_3)):
    line = line_list_3[idx]
    pick_lines_3.append(line)

if normal_run == 1:
#get sample
    for j in range(len(pick_lines_3)):
        x = pick_lines_3[j]
        for k in range(len(x)):
            if x[k].isdigit():
                sample_list_3.append(int(x[k]))
                sample_list_3_show.append(int(x[k]) - 20)
#training  sequnce
else:
    for x in range(0,288,1):
        sample_list_3.append(random.randint(0,1))
        sample_list_3_show.append(sample_list_3[x] -20) 

#expand for better show
for j in range(len(sample_list_3_show)):
    if sample_list_3_show[j] == -20:
        sample_list_3_show[j] = sample_list_3_show[j] - 4

#1-0 delt_4 analyze
for i in range(len(sample_list_3)):
    if(sample_list_3[i] == 1):
        one = one +1
    if(sample_list_3[i] == 0):
        zero = zero + 1
    delt_3.append((one-zero) - 20)
    #print("[1]=%d [0]=%d 0-1=%d" %(one,zero,one-zero))


#get all lines
for idx in range(len(line_list_2)):
    line = line_list_2[idx]
    pick_lines_2.append(line)

if normal_run == 1:
#get sample
    for j in range(len(pick_lines_2)):
        x = pick_lines_2[j]
        for k in range(len(x)):
            if x[k].isdigit():
                sample_list_2.append(int(x[k]))
                sample_list_2_show.append(int(x[k]) - 10)

#training  sequnce
else:
    for x in range(0,288,1):
        sample_list_2.append(random.randint(0,1))
        sample_list_2_show.append(sample_list_2[x] -10) 
            

#expand for better show
for j in range(len(sample_list_2_show)):
    if sample_list_2_show[j] == -10:
        sample_list_2_show[j] = sample_list_2_show[j] - 4

#1-0 delt_4 analyze
for i in range(len(sample_list_2)):
    if(sample_list_2[i] == 1):
        one = one +1
    if(sample_list_2[i] == 0):
        zero = zero + 1
    delt_2.append((one-zero) - 5)
    #print("[1]=%d [0]=%d 0-1=%d" %(one,zero,one-zero))

###############################################################################
#get all lines
for idx in range(len(line_list_1)):
    line = line_list_1[idx]
    pick_lines_1.append(line)

if normal_run == 1:
#get sample
    for j in range(len(pick_lines_1)):
        x = pick_lines_1[j]
        for k in range(len(x)):
            if x[k].isdigit():
                sample_list_1.append(int(x[k]))
                sample_list_1_show.append(int(x[k]) )

#training  sequnce
else:
    for x in range(0,288,1):
        sample_list_1.append(random.randint(0,1))
        sample_list_1_show.append(sample_list_1[x]) 
            


#expand for better show
for j in range(len(sample_list_1_show)):
    if sample_list_1_show[j] == 0:
        sample_list_1_show[j] = sample_list_1_show[j] - 4

#1-0 delt_4 analyze
for i in range(len(sample_list_1)):
    if(sample_list_1[i] == 1):
        one = one +1
    if(sample_list_1[i] == 0):
        zero = zero + 1
    delt_1.append((one-zero) - 5)
    #print("[1]=%d [0]=%d 0-1=%d" %(one,zero,one-zero))
    

###############################################################################
#get all lines
for idx in range(len(line_list_0)):
    line = line_list_0[idx]
    pick_lines_0.append(line)

if normal_run == 1:
#get sample
    for j in range(len(pick_lines_0)):
        x = pick_lines_0[j]
        for k in range(len(x)):
            if x[k].isdigit():
                sample_list_0.append(int(x[k]))
                sample_list_0_show.append(int(x[k]) + 10)

#training  sequnce
else:
    for x in range(0,288,1):
        sample_list_0.append(random.randint(0,1))
        sample_list_0_show.append(sample_list_0[x] + 10) 
            

#expand for better show
for j in range(len(sample_list_4_show)):
    if sample_list_0_show[j] == 10:
        sample_list_0_show[j] = sample_list_0_show[j] - 4

#1-0 delt_4 analyze
for i in range(len(sample_list_0)):
    if(sample_list_0[i] == 1):
        one = one +1
    if(sample_list_0[i] == 0):
        zero = zero + 1
    delt_0.append((one-zero) - 5)
    #print("[1]=%d [0]=%d 0-1=%d" %(one,zero,one-zero))


if normal_run == 1:
    print("---win in file",file_path_4)
else:
    print("---win in self test\n")


plt.plot(sample_list_4_show,color='green',marker='.',label ='smp-4')
plt.plot(sample_list_3_show,color='red',marker='.',label ='smp-3')
plt.plot(sample_list_2_show,color='brown',marker='.',label ='smp-2')
plt.plot(sample_list_1_show,color='darkblue',marker='.',label ='smp-1')
plt.plot(sample_list_0_show,color='black',marker='.',label ='smp-0')

#plt.plot(delt_4,color='green',marker='.',label ='delt_4(1-0):%d'%(one-zero))

#plt.plot(delt_3,color='red',marker='.',label ='delt_4(1-0):%d'%(one-zero))


#plt.plot(win_1_list,color='brown',marker='.',label ='win_1')
#plt.plot(win_0_list,color='darkblue',marker='.',label ='win_0')

#plt.plot(long_zero,color='brown',marker='.',label ='L0=%d [0]=%d' % (,zero))
#plt.plot(long_one,color='darkblue',marker='.',linestyle=':',label ='L1=%d [1]=%d' % (,one))
#plt.plot(long_x0,color='black',marker='.',linestyle=':',label ='L0 dist')
#plt.plot(long_x1,color='cyan',marker='.',label ='L1 dist')

plt.legend(loc='best', fontsize=8)
plt.show()


log_4.close()
log_3.close()
log_2.close()
log_1.close()
log_0.close()
 
print("end .....")

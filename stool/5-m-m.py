import re
import matplotlib.pyplot as plt
import random
import numpy as np
import matplotlib as mpl



file_path = "./0809-4.txt"
print("start.....")
log = open(file_path,"r")
#
result_file = open("./5-m-m-result","w")
pick_lines = []
smp_rst = []
predict = []
x = []
one = 0
zero =0
delt = []
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

for i in range(len(smp_rst)):
    if(smp_rst[i] == 1):
        one = one +1
    if(smp_rst[i] == 0):
        zero = zero + 1
    delt.append((one-zero))
    print("[1]=%d [0]=%d 0-1=%d" %(one,zero,one-zero))
plt.plot(smp_rst,color='green',marker='.',label ='true')
plt.plot(delt,color='red',marker='.',label ='true')

plt.show()

log.close()
#result_file.close()

            
print("end .....")

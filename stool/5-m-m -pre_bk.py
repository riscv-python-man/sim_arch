import re
import matplotlib.pyplot as plt
import random
import numpy as np
import matplotlib as mpl



file_path = "d:\\zqh\\0809-4.txt"
print("start.....")
log = open(file_path,"r")
#
result_file = open("d:\\zqh\\5-m-m-result","w")
pick_lines = []
smp_rst = []
predict = []
x = []
s = 0
one = 0
zero =0
do_it_0 = []
do_it_1 = []
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
            if(x[k] == '1'):
                one = one +1
            if(x[k] == '0'):
                zero = zero + 1

n =  len(smp_rst)             
for j in range(n,288,1):
    smp_rst.append(random.randint(0, 1))

print("0= %d 1= %d"%(zero,one))
                    
print("smaple data...")  
print(smp_rst)

for m in range(0,288,1):
    predict.append(random.randint(0, 1) + 2)

print("predict data...")
print(predict) 

    
# plot output 
q = []
n_0 = 0
n_1 = 0
for m in range(len(smp_rst)):
    q.append(m)
    #print(q[m], smp_rst[m])
    
s =0
for m in range(0,len(smp_rst),1):
    if predict[m]-2 ==  smp_rst[m]:
        s = s +1
        if predict[m]-2 == 0:
            do_it_0.append(m+1)
        else:
            do_it_1.append(m+1)
        
    if predict[m]-2 == 0:
        n_0 = n_0 +1
    else:
        n_1 = n_1 +1
    
print("a=b is %d 0=%d 1=%d"%(s,n_0,n_1))        

print("do_it_0 is...")
print(do_it_0)
print("do_it_1 is...")
print(do_it_1)
#result_file.writelines(" ".join(str(i) for i in do_it))

plt.plot(q,smp_rst,color='green',marker='.',label ='true')
plt.plot(q,predict,color='red',marker='.',label ='predict')


#plt.scatter(q,smp_rst)
#plt.scatter(q,predict)

plt.show()

log.close()
result_file.close()

            
print("end .....")

import re
import matplotlib.pyplot as plt

file_path = "./thr_log_file.txt"
print("throughput plot...")
log = open(file_path,"r")

pick_lines = []
rst = []
k = ''
s = 0
line_list = log.readlines()

#get all lines
for idx in range(len(line_list)):
    line = line_list[idx]
    #if("Mbits/sec" in line and "SUM" in line):
    if("/sec" in line and "sec" in line):
        pick_lines.append(line)

#get sub string : "MBytes   239 Mbits/sec"
for j in range(len(pick_lines)):
    x = pick_lines[j]
    y = x.find("Bytes")
    z = x[y:]
    #get digit from sub string
    for j in range(len(z)): 
        t = z[j]
        if(t.isdigit() or t == '.'):
               k = k + t
               s = float(k)
    if(z[-10] == 'K'):
        s = s * 0.001
    rst.append(s)
    k=''

# plot output 
q = []
for m in range(len(rst)):
    q.append(m)
    #print(q[m], rst[m])

plt.text(-5,210,"Y:Mbps   X:MCS/10s")
plt.plot(q, rst)
#plt.scatter(q,rst)
plt.show()

log.close()
#result_file.close()
            

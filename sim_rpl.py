import os
import re

s_out = []
f = open("rpl_in.txt", "r")
lines = f.readlines()
for line in lines:
    s_out = re.split(' ', line)
    s_old = s_out[0].strip()
    s_new = s_out[1].strip()
    
    os.system("sed -i 's/%s/%s/g' *.h *.c" % (s_old,s_new))
    
f.close()

print ("replace ok")

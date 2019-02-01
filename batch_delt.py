import os

f = open("delt_item.txt", "r")
lines = f.readlines()
for line in lines:
    s = line.strip()
    os.system("sed -i '/%s/d' *.h" % (s))
    
f.close()

print ("batch delt ok")

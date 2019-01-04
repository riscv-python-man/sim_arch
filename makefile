cc   = gcc
tag  = 0
deps = $(shell find ./ -name "*.h")
src  = $(shell find ./ -name "*.c")
obj  = $(src:%.c=%.o)# it's a replace... 

$(tag):$(obj)
	$(cc) -o $(tag) $(obj) -lpthread

%.o:%.c $(deps)
	$(cc) -c $< -o $@  -lpthread

.PHONY: co
co:
	rm -rf $(obj)

.PHONY: ca
ca:
	rm -rf $(tag) $(obj)

import os
wifi_c_file = []
wifi_h_file = []
define_list = []
def get_target_dir_path():
    file = os.path.abspath(os.curdir)
    for root, dirs, files in os.walk(file):
        if len(files) != 0:
            for fil in files:
                if ".c" in fil:
                    if ".o.cmd" in fil:
                        continue
                    elif ".ko.cmd" in fil:
                        continue
                    elif ".mod.c" in fil:
                        continue
                    wifi_c_file.append(fil)
                elif ".h" in fil:
                    wifi_h_file.append(fil)
def search_macro_definition():
    temp_list = []
    for file in wifi_h_file:
        with open(file,"r") as f_h:
            f_h_data = f_h.readlines()
            for data in f_h_data:
                if "#define" in data:
                    if "//" in data:
                        continue
                    elif "_H" in data:
                        continue
                    with open("define_result.txt","a+") as define_file:
                        define_file.writelines(data.strip().split("#define")[1].strip()+"\n")

    with open("define_result.txt","r") as f:
        for i in f.readlines():
            for element in i:
                if element is " ":
                    break
                elif element is "(":
                    break
                elif element is "\t":
                    break
                temp_list.append(element)
            define_list.append("".join(temp_list))
            temp_list.clear()

def compare_macro_definition():
    all_files_list = []
    define_be_used_time = {}
    all_files_list.extend(wifi_c_file)
    all_files_list.extend(wifi_h_file)
    for define in define_list:
        define_be_used_count = 0
        for file in all_files_list:
            with open(file, "r") as file_f:
                string_from_file_list = file_f.readlines()
                for  string in string_from_file_list:
                    if  string.find(define) != -1:
                        define_be_used_count += 1
                        print("%s is used in flie:%s"%(define,file))
        define_be_used_time[define] = define_be_used_count
    with open("result.txt", "a+") as f_result:
        for i in define_list:
            define_used_time = define_be_used_time[i]
            if define_used_time > 1:
                continue
            f_result.write(i+"\n")

if __name__ == "__main__":
    get_target_dir_path()
    search_macro_definition()
    compare_macro_definition()
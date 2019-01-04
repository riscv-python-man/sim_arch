import serial
import threading
import time
import os
import queue
def ping_function_decorator(function):
    def wrapper(self,*args,**kwargs):
        self.STA_COM.write(chr(0x03).encode())
        self.AP_COM.write(chr(0x03).encode())
        function(self,*args,**kwargs)
        self.AP_COM.write(self.ping_command.encode())
        time.sleep(2)
        for i in range(5):
            time.sleep(1)
            if not self.ping_result.empty():
                print("%s\n"%self.ping_result.get())
                break
            elif i > 3:
                self.STA_COM.write(chr(0x03).encode())
                self.AP_COM.write(chr(0x03).encode())
                print("Ping no pass!\n")
                self.ping_no_pass = True
                return False
        self.STA_COM.write(chr(0x03).encode())
        self.AP_COM.write(chr(0x03).encode())
    return wrapper
class B2B_function_test(object):
    def __init__(self, AP_COM, STA_COM):
        self.AP_COM = serial.Serial(AP_COM, 115200, timeout=1)
        self.STA_COM = serial.Serial(STA_COM, 115200, timeout=1)
        self.timestamp = time.strftime('%Y_%m_%d_%H_%M', time.localtime(time.time()))
        self.ap_fullog_file_path = "E:\\ap_full_log_%s.txt" % self.timestamp
        self.sta_fullog_file_path = "E:\\sta_full_log_%s.txt" % self.timestamp
        self.ap_fullog_file = open(self.ap_fullog_file_path,"w")
        self.sta_fullog_file = open(self.sta_fullog_file_path, "w")
        self.hold_test_parameters = []
        self.test_time = 120
        self.ap_log_flag = 1
        self.sta_log_flag = 1
        self.ping_no_pass = False
        self.ap_init_flag = queue.Queue()
        self.sta_init_flag = queue.Queue()
        self.ap_rmmod_flag = queue.Queue()
        self.sta_rmmod_flag = queue.Queue()
        self.connect_flag = queue.Queue()
        self.ap_hostapd_up_flag = queue.Queue()
        self.ping_result = queue.Queue()
        self.ap_ip_addr = "192.168.1.88"
        self.sta_ip_addr = "192.168.1.99"
        self.ping_command = "ping %s\n" % self.sta_ip_addr
        self.su_command = "su\r\n mount -o rw,remount /system\r\n\n"
        self.kill_hostapd = "killall hostapd\r\n"
        self.rmmod_command = "rmmod 8192cu.ko\r\n"
        self.set_pri_channel_command = "iw dev wlan0 vendor send 0xc3 0xc4 0x0a 0x00 0x00 0x2e 0x2c "
        self.ap_init_command = "insmod /system/lib/8192cu.ko " \
                               "mac_addr=00:01:02:58:00:12;ifconfig " \
                               "wlan0 %s up;\r\n" % self.ap_ip_addr
        self.sta_init_command = "insmod /system/lib/8192cu.ko " \
                                "mac_addr=00:01:02:58:00:13;" \
                                "ifconfig wlan0 %s up;\r\n" % self.sta_ip_addr
        self.test_channel_rate = {"vht80M": [[157, ], [0,1,2,3,4,5,6,7,8,9]], "vht40M": [[157, ], [0,1,2,3,4,5,6,7,8,9]],
                                  "vht20M": [[157, ], [0,1,2,3,4,5,6,7]], "ht40M": [[157, ], [0,1,2,3,4,5,6,7]],
                                  "ht20M": [[157, ], [0,1,2,3,4,5,6,7]], "11g": [[6, ], [6,9,12,18,24,36,48,54]],
                                  "11b": [[6, ], [1,2,5.5,11]]}
        self.vht_ht_pri_channel = {"vht80M": {153: "0xa2 0x00 0x00 0x00",
                                               157: "0xa1 0x00 0x00 0x00"},
                                   "vht40M": {153: "0x91 0x00 0x00 0x00",
                                               157: "0x92 0x00 0x00 0x00"},
                                   "vht20M": {153: "0x80 0x00 0x00 0x00",
                                               157: "0x80 0x00 0x00 0x00"},
                                   "ht40M": {153: "0x91 0x00 0x00 0x00",
                                              157: "0x92 0x00 0x00 0x00"},
                                   "ht20M": {153: "0x80 0x00 0x00 0x00",
                                              157: "0x80 0x00 0x00 0x00"},
                                   "11b": {6: "0x80 0x00 0x00 0x00",
                                           11: "0x80 0x00 0x00 0x00"},
                                   "11g": {6: "0x80 0x00 0x00 0x00",
                                           11: "0x80 0x00 0x00 0x00"}}
        self.hostapd_up_file_path = {153: "hostapd -B -d /system/etc/wifi/B2B_Verify_config/",
                                     157: "hostapd -B -d /system/etc/wifi/",
                                     6: "hostapd -B -d /system/etc/wifi/B2B_Verify_config/",
                                     11: "hostapd -B -d /system/etc/wifi/"}
        self.set_rate_command = {"vht": "iw dev wlan0 set bitrates vht-mcs-2.4 1:",
                                 "ht": "iw dev wlan0 set bitrates ht-mcs-2.4 ",
                                 "11b_11g": "iw dev wlan0 set bitrates legacy-2.4 "}
        self.iperf_command = {"TCP": {"AP": "iperf -c %s -i 1 -t %d\r\n" % (self.sta_ip_addr, self.test_time),
                                      "STA": "iperf -s -i 1\r\n"},
                              "UDP": {
                                  "AP": "iperf -c %s -i 1 -t %d -u -b 500M\r\n" % (self.sta_ip_addr, self.test_time),
                                  "STA": "iperf -s -i 1 -u\r\n"}}
    def ap_sta_init(self):
        self.AP_COM.write(self.su_command.encode())
        self.STA_COM.write(self.su_command.encode())
        time.sleep(1)
        self.AP_COM.write(self.ap_init_command.encode())
        for i in range(15):
            time.sleep(1)
            if not self.ap_init_flag.empty():
                print("AP %s initialization!\n"%self.ap_init_flag.get())
                self.ap_init_flag.queue.clear()
                break
            if i > 13 :
                print("AP failed initialization!\n")
                return False
        self.STA_COM.write(self.sta_init_command.encode())
        for i in range(15):
            time.sleep(1)
            if not self.sta_init_flag.empty():
                print("STA %s initialization!\n"%self.sta_init_flag.get())
                self.sta_init_flag.queue.clear()
                break
            if i > 13 :
                print("STA failed initialization!\n")
                return False
        time.sleep(1)
        return True
    def set_init_parameter(self, test_mode, ch):
        # ap hostapd up
        self.ap_hostapd_command = self.hostapd_up_file_path[ch] + "hostapd_%s.conf" % test_mode + "\r\n"
        self.AP_COM.write(self.ap_hostapd_command.encode())
        print(self.ap_hostapd_command)
        for i in range(15):
            time.sleep(1)
            if not self.ap_hostapd_up_flag.empty():
                print(self.ap_hostapd_up_flag.get() + "\n")
                self.ap_hostapd_up_flag.queue.clear()
                break
            if i > 13:
                print("AP hostapd up failed!\n")
                return False
        time.sleep(2)
        # set sta pri channel
        self.sta_pri_channel_command = self.set_pri_channel_command + self.vht_ht_pri_channel[test_mode][ch] + "\r\n"
        self.STA_COM.write(self.sta_pri_channel_command.encode())
        print("STA set pri channel-->%s"%self.sta_pri_channel_command)
        time.sleep(2)
        self.STA_COM.write(chr(0x03).encode())
        self.AP_COM.write(chr(0x03).encode())
        time.sleep(1)
        return True
    #@ping_function_decorator
    def set_test_rate(self, test_mode, rate):
        if "vht" in test_mode:
            self.rate_index = "vht"
        elif "ht" in test_mode:
            self.rate_index = "ht"
        elif "11g" in test_mode:
            self.rate_index = "11b_11g"
        elif "11b" in test_mode:
            self.rate_index = "11b_11g"
        else:
            print("Rate index error!\n")
        self.set_test_rate_command = self.set_rate_command[self.rate_index] + str(rate) + "\r\n"
        print(self.set_test_rate_command)
        self.AP_COM.write(self.set_test_rate_command.encode())
        time.sleep(1)
        self.STA_COM.write(self.set_test_rate_command.encode())
        time.sleep(1)
    def send_iperf_command(self, type_data):
        print("-*-*-*-*-*-*-*-*-*-*-*-*- %s -*-*-*-*-*-*-*-*-*-*-*-"%type_data)
        self.send_sta_iperf_command = self.iperf_command[type_data]["STA"] + "\r\n"
        self.STA_COM.write(self.send_sta_iperf_command.encode())
        time.sleep(2)
        self.send_ap_iperf_command = self.iperf_command[type_data]["AP"] + "\r\n"
        self.AP_COM.write(self.send_ap_iperf_command.encode())
        time.sleep(3)
    def sta_connect_ap(self):
        time.sleep(5)
        self.connect_command = "iw dev wlan0 connect lg_test\r\n"
        self.STA_COM.write(self.connect_command.encode())
        for i in range(35):
            time.sleep(1)
            if not self.connect_flag.empty():
                print(self.connect_flag.get() + "\n")
                self.connect_flag.queue.clear()
                break
            elif i > 33:
                print("STA connected AP failed!\n")
                return False
        time.sleep(1)
        self.STA_COM.write(chr(0x03).encode())
        self.AP_COM.write(chr(0x03).encode())
        time.sleep(1)
        return True
    def rmmod_sta_ap(self):
        self.ap_killhostapd_command = "killall hostapd\r\n"
        self.rmmod_command = "rmmod 8192cu.ko\r\n"
        self.STA_COM.write(self.rmmod_command.encode())
        for i in range(15):
            time.sleep(1)
            if not self.sta_rmmod_flag.empty():
                print(self.sta_rmmod_flag.get()+"\n")
                self.sta_rmmod_flag.queue.clear()
                break
            if i > 13:
                print("STA rmmod failed!\n")
                return False
        self.AP_COM.write(self.ap_killhostapd_command.encode())
        time.sleep(5)
        self.AP_COM.write(self.rmmod_command.encode())
        for i in range(15):
            time.sleep(1)
            if not self.ap_rmmod_flag.empty():
                print(self.ap_rmmod_flag.get()+"\n")
                self.ap_rmmod_flag.queue.clear()
                break
            if i > 13:
                print("AP rmmod failed!\n")
                return False
        return True
    def print_ap_log_info(self):
        while self.ap_log_flag:
            if self.AP_COM.isOpen():
                self.ap_comm_info = self.AP_COM.readline()
                if "wifi_mac_hardstart" in self.ap_comm_info.decode():
                    self.ap_init_flag.put("successful")
                elif "exit_aml_sdio" in self.ap_comm_info.decode():
                    self.ap_rmmod_flag.put("AP rmmod successfully!")
                elif "state SCAN->CONNECTED" in self.ap_comm_info.decode():
                    self.ap_hostapd_up_flag.put("AP hostapd up successfully!")
                elif "bytes from %s"%self.sta_ip_addr in self.ap_comm_info.decode():
                    self.ping_result.put("ping successfully")
                    print(self.ap_comm_info.decode())
            self.ap_fullog_file.writelines(self.ap_comm_info.decode())
    def print_sta_log_info(self):
        while self.sta_log_flag:
            if self.STA_COM.isOpen():
                self.sta_comm_info = self.STA_COM.readline()
                if "wifi_mac_hardstart" in self.sta_comm_info.decode():
                    self.sta_init_flag.put("successful")
                elif "ASSOC->CONNECTED" in self.sta_comm_info.decode():
                    self.connect_flag.put("STA connected AP successfully!")
                elif "Mbits/sec" in self.sta_comm_info.decode():
                    print(self.sta_comm_info.decode())
                elif "Kbits/sec" in self.sta_comm_info.decode():
                    print(self.sta_comm_info.decode())
                elif "exit_aml_sdio" in self.sta_comm_info.decode():
                    self.sta_rmmod_flag.put("STA rmmod successfully!")
            self.sta_fullog_file.writelines(self.sta_comm_info.decode())
    def print_sta_ap_thread(self):
        self.thread_arrg = []
        self.ap_print = threading.Thread(target=self.print_ap_log_info)
        self.sta_print = threading.Thread(target=self.print_sta_log_info)
        self.thread_arrg.append(self.ap_print)
        self.thread_arrg.append(self.sta_print)
        for t in self.thread_arrg:
            t.setDaemon(True)
            t.start()
    def start_test(self):
        print("-*-*-*-*-*-*-Wifi Verify start-*-*-*-*-*-*-*-*\n")
        self.test_case = ["vht20M"]
        self.print_sta_ap_thread()
        for case in self.test_case:
            for channel in self.test_channel_rate[case][0]:
                self.ap_sta_init()
                self.set_init_parameter(case, channel)
                if self.sta_connect_ap():
                    for rate in self.test_channel_rate[case][1]:
                        self.STA_COM.write(chr(0x03).encode())
                        self.AP_COM.write(chr(0x03).encode())
                        self.set_test_rate(case, rate)
                        if "vht" in case:
                            print("Test mode-->%s Test channel--> %d,test rate-->MCS%d"%(case,channel,rate))
                        elif "ht" in case:
                            print("Test mode-->%s Test channel--> %d,test rate-->MCS%d" % (case, channel, rate))
                        else:
                            print("Test mode-->%s Test channel--> %d,test rate-->Legacy %d" % (case,channel, rate))
                        for data in ["TCP", "UDP"]:
                            self.STA_COM.write(chr(0x03).encode())
                            self.AP_COM.write(chr(0x03).encode())
                            self.send_iperf_command(data)
                            time.sleep(self.test_time+2)
                            self.STA_COM.write(chr(0x03).encode())
                            self.AP_COM.write(chr(0x03).encode())
                    self.rmmod_sta_ap()
                else:
                    self.hold_test_parameters.append((case,channel,["TCP", "UDP"],self.test_channel_rate[case][1]))
                    print("Test mode-->%s Test channel-->%d\n"%(case,channel))
                    print("Parameters are saved!Wait for double checking!\n")
                    self.rmmod_sta_ap()
        if len(self.hold_test_parameters) > 0:
            for err_parameters in self.hold_test_parameters:
                self.double_check(err_parameters[0],err_parameters[1],err_parameters[2],err_parameters[3])
                self.hold_test_parameters.remove(err_parameters)
        else:
            self.close_file_function()
    def close_file_function(self):
        self.ap_log_flag = 0
        self.sta_log_flag = 0
        time.sleep(2)
        self.ap_fullog_file.close()
        self.sta_fullog_file.close()
        self.AP_COM.close()
        self.STA_COM.close()
    def double_check(self,tesmode,channel,typedata,ratelist):
        print("Now is checking error data.\n")
        self.print_sta_ap_thread()
        self.ap_sta_init()
        self.set_init_parameter(tesmode, channel)
        self.sta_connect_ap()
        for rate in ratelist:
            self.set_test_rate(tesmode, rate)
            if "vht" in tesmode:
                print("Test mode-->%s Test channel--> %d,test rate-->MCS%d" % (tesmode, channel, rate))
            elif "ht" in tesmode:
                print("Test mode-->%s Test channel--> %d,test rate-->MCS%d" % (tesmode, channel, rate))
            else:
                print("Test mode-->%s Test channel--> %d,test rate-->Legacy %d" % (tesmode, channel, rate))
            for data in typedata:
                self.STA_COM.write(chr(0x03).encode())
                self.AP_COM.write(chr(0x03).encode())
                self.send_iperf_command(data)
                time.sleep(self.test_time + 2)
                self.STA_COM.write(chr(0x03).encode())
                self.AP_COM.write(chr(0x03).encode())
        self.rmmod_sta_ap()
        self.close_file_function()
if __name__ == "__main__":
    b2b_test = B2B_function_test("COM7", "COM4")
    b2b_test.start_test()
    #b2b_test.double_check("ht_40",6,["TCP","UDP"],[48,54])



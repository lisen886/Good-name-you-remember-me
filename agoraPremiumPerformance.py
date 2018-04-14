# -*- coding: utf-8 -*-
import os,subprocess,platform,re,time
PATH = lambda p: os.path.abspath(p)

# 判断系统类型，windows使用findstr，linux使用grep
system = platform.system()
if system is "Windows":
    find_util = "findstr"
else:
    find_util = "grep"
if "ANDROID_HOME" in os.environ:
    if system == "Windows":
        command = os.path.join(
            os.environ["ANDROID_HOME"],
            "platform-tools",
            "adb.exe")
    else:
        command = os.path.join(
            os.environ["ANDROID_HOME"],
            "platform-tools",
            "adb")
else:
    raise EnvironmentError(
        "Adb not found in $ANDROID_HOME path: %s." %
        os.environ["ANDROID_HOME"])

class performance:
    """
    summary: 单个设备，可不传入参数device_id
    return:
    author: lisen sui
    """
    def __init__(self, device_id=""):
        if device_id == "":
            self.device_id = ""
        else:
            self.device_id = "-s %s" % device_id

    def adb(self, args):
        cmd = "%s %s %s" % (command,self.device_id, str(args))
        return subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    def shell(self, args):
        cmd = "%s %s shell %s" % (command, self.device_id, str(args),)
        return subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    """
    summary: 获取设备id号
    return:
    author: lisen sui
    """
    def get_device_id(self):
        return self.adb("get-serialno").stdout.read().strip()
    """
    summary: 获取设备中的Android版本号
    return:
    author: lisen sui
    """
    def get_android_version(self):
        return self.shell(
            "getprop ro.build.version.release").stdout.read().strip()
    """
    summary: 获取当前应用界面的包名和Activity
    return:
    author: lisen sui
    """
    def __get_package_and_activity(self):
        out = self.shell(
            "dumpsys activity activities | %s mFocusedActivity" %
            find_util).stdout.read().strip().split(' ')[3]
        return out
    def get_current_package_name(self):
        """
        获取当前运行的应用的包名
        """
        package_name = self.__get_package_and_activity().split("/")[0]
        print ("current package_name is:%s"%package_name)
        return package_name

    def get_current_activity(self):
        """
        获取当前运行应用的activity
        """
        return self.__get_package_and_activity().split("/")[1]
    def get_battery_level(self):
        """
        获取电池电量
        """
        levels = self.shell("dumpsys battery | %s level" %find_util).stdout.read()
        currenLevel = levels.split("\n")[0]
        level = currenLevel.split(": ")[-1]
        print ("current power level:%s%%"%int(level))
        return int(level)
    def get_battery_temp(self):
        """
        获取电池温度
        """
        temp = self.shell("dumpsys battery | %s temperature" %find_util).stdout.read().split(": ")[-1]
        return int(temp) / 10.0
    """
    summary: 获取当前APP cpu百分比
    return:
    author: lisen sui
    """
    def get_cpu(self, package_name):
        if package_name == 'com.tencent.mm':
            WeChatPNTool = 'com.tencent.mm:tools'
            WeChatcmdCPU = '''top -n 1|%s %s|awk -F'%%' '{print $1}' ''' % (find_util, WeChatPNTool)
            agora = self.shell(WeChatcmdCPU)
            WeChatstr = agora.stdout.read()
            WeChatlist = WeChatstr.split(" ")
            WeChatnum = len(WeChatlist)
            WeChatcpu = float(WeChatlist[WeChatnum - 1])
            print('WeChatToolsCPU: %d%%' % float(WeChatcpu))
            return WeChatcpu
        else:
            cmdCPU = '''top -n 1|%s %s|awk -F'%%' '{print $1}' ''' % (find_util, package_name)
            agora = self.shell(cmdCPU)
            str = agora.stdout.read()
            list = str.split(" ")
            num = len(list)
            cpu = float(list[num - 1])
            print('cpu: %d%%' % float(cpu))
            return cpu
    """
    summary: 获取当前APP内存
    return:
    author: lisen sui
    """
    def get_memory(self, package_name):
        cmdIfMem = '''dumpsys meminfo %s|%s TOTAL:''' % (package_name, find_util)
        cmdMemory = '''dumpsys meminfo %s|%s TOTAL:|awk -F' ' '{print $2}' ''' % (package_name, find_util)
        cmdMemory2 = '''dumpsys meminfo %s|%s TOTAL|awk -F' ' '{print $2}' ''' % (package_name, find_util)
        agoraIf = self.shell(cmdIfMem).stdout.read()
        if "TOTAL:" in agoraIf:
            agora = self.shell(cmdMemory)
            memory = int(agora.stdout.read())
            print('memory: %d' % (memory) + 'KB')
            print('内存使用:%dMB' % ((memory) / 1024))
            return memory
        else:
            agora2 = self.shell(cmdMemory2)
            memory2 = int(agora2.stdout.read())
            print('memory: %d' % (memory2) + 'KB')
            print('内存使用:%dMB' % ((memory2) / 1024))
            return memory2
    """
    summary: 获取全部内存
    return:
    author: lisen sui
    """
    def get_memory_total(self):
        total = self.shell('cat proc/meminfo')
        while True:
            r = total.stdout.readline().strip().decode('utf-8')
            if r and 'MemTotal' in r:
                lst = [MemTotal for MemTotal in r.split(' ') if MemTotal]
                return int(lst[1])
    """
    summary: 获取当前内存占用百分比
    return:
    author: lisen sui
    """
    def get_memory_percent(self, package_name):
        try:
            percent =float(self.get_memory(package_name)/float(self.get_memory_total()) * 100)
            print ("memory percent is : %.2f%%"%percent)
            return percent
        except:
            return None
    def get_appId(self, package_name):
        appidInfo = self.shell("ps | %s %s"%(find_util, package_name)).stdout.read().strip()
        appidStr = appidInfo.split(" ")[0]
        # 删除(_)的字符串
        num = re.sub(r'_', "", appidStr)
        return num
    """
    summary: 测试cpu、内存的平均值
    return: cpu memory
    author: lisen sui
    """
    def cpuAndMemory(self,num,package_name):
        print ('==============cpu and memory test================')
        cpuTotal = 0
        memoryTotal = 0
        for i in range(int(num)):
            cpu = self.get_cpu(package_name)
            cpuTotal += float(cpu)
            memory = self.get_memory(package_name)
            memoryTotal += memory
            print ('---------------')
        print('CPU平均值:%d%%' % (cpuTotal / int(num)))
        print('平均内存使用:%d MB' % ((memoryTotal / float(num)) / 1024))

    """
    summary: 耗电（使用adb tcpip 5555无线连接Android）
    return:
    author: lisen sui
    """
    def consume_power(self,minute,package_name):
        print ('==============consume power test=================')
        start_battery_level = int(self.get_battery_level())
        reset = self.shell("dumpsys batterystats --reset").stdout.read().strip()
        print (reset)
        time.sleep(minute*60)
        stop_battery_level = int(self.get_battery_level())
        consume_battrey_level = start_battery_level-stop_battery_level
        str = self.shell("dumpsys batterystats | less").stdout.read().split("Estimated power use (mAh):")
        appPowerInfo = str[1].split("\n")[2]
        if self.get_appId(package_name) in appPowerInfo:
            print ("app consume power:%smAh"%appPowerInfo.split(" ")[6])
            print ("app consume power percent:%s%%"%consume_battrey_level)
        else:
            print ("app can't running")
        # str = self.shell("dumpsys batterystats | less").stdout.readlines()
        # for line in str:
        #     if "Estimated power use (mAh)" in line:
        #         print ("info:%s"%line)

    def get_pid(self, package_name):
        """
        获取进程pid
        args:
        - packageName -: 应用包名
        """
        if system is "Windows":
            pidinfo = self.shell(
                "ps | findstr %s$" %
                package_name).stdout.read()
        else:
            pidinfo = self.shell(
                "ps | %s -w %s" %
                (find_util, package_name)).stdout.read()

        if pidinfo == '':
            return "the process doesn't exist."

        pattern = re.compile(r"\d+")
        result = pidinfo.split(" ")
        result.remove(result[0])

        return pattern.findall(" ".join(result))[0]
    def get_uid(self, pid):
        """
        获取uid
        :param pid:
        :return:
        """
        result = self.shell("cat /proc/%s/status" % pid).stdout.readlines()
        for i in result:
            if 'uid' in i.lower():
                return i.split()[1]

    def get_flow_data_tcp(self, uid):
        """
        获取应用tcp流量
        :return:(接收流量（tcp_rcv）和发送流量（tcp_snd）)
        """
        tcp_rcv = self.shell("cat proc/uid_stat/%s/tcp_rcv" % uid).stdout.read().split()[0]
        tcp_snd = self.shell("cat proc/uid_stat/%s/tcp_snd" % uid).stdout.read().split()[0]
        tcp_rcv_KB = float(tcp_rcv)/1024
        tcp_snd_KB = float(tcp_snd)/1024
        print ("tcp_rcv:%s KB ,tcp_snd:%s KB" % (tcp_rcv_KB,tcp_snd_KB))
        return tcp_rcv, tcp_snd
    '''
     rx_bytes（接收数据）和tx_bytes（传输数据）
    '''
    def get_rx(self,uid):
        rx_bytes_total = 0
        byte = self.shell("cat /proc/net/xt_qtaguid/stats |%s %s" % (find_util, uid)).stdout.readlines()
        for i in range(0, len(byte)):
            rx_bytes = float(byte[i].split(" ")[5])
            rx_bytes_total += rx_bytes
        return int(rx_bytes_total/1024)
    def get_tx(self,uid):
        tx_bytes_total = 0
        byte = self.shell("cat /proc/net/xt_qtaguid/stats |%s %s" % (find_util, uid)).stdout.readlines()
        for i in range(0, len(byte)):
            tx_bytes = float(byte[i].split(" ")[7])
            tx_bytes_total += tx_bytes
        return int(tx_bytes_total/1024)
    '''
    获取App从新开进程到目前的总消耗带宽
    '''
    def get_rx_tx(self,uid):
        rx_bytes_total = 0
        tx_bytes_total = 0
        byte = self.shell("cat /proc/net/xt_qtaguid/stats |%s %s" % (find_util,uid)).stdout.readlines()
        for i in range(0,len(byte)):
            rx_bytes = float(byte[i].split(" ")[5])
            tx_bytes = float(byte[i].split(" ")[7])
            rx_bytes_total += rx_bytes
            tx_bytes_total += tx_bytes
        print ("rx_bytes:%sKB,≈%.2fMB"%((int(rx_bytes_total/1024)),(float(rx_bytes_total/1024/1024))))
        print ("tx_bytes:%sKB,≈%.2fMB"%((int(tx_bytes_total/1024)),(float(tx_bytes_total/1024/1024))))
    """
    summary: 每隔一秒获取一次rx/tx
    return: 网速
    author: lisen sui
    """
    def get_network_speed_rx(self,uid):
        first_rx = self.get_rx(uid)
        time.sleep(1)
        last_rx = self.get_rx(uid)
        speed_rx = last_rx-first_rx
        print ("speed_rx :%sKb/s" % (speed_rx*8))
        return float(speed_rx*8)
    def get_network_speed_tx(self,uid):
        first_tx = self.get_tx(uid)
        time.sleep(1)
        last_tx = self.get_tx(uid)
        speed_tx = last_tx-first_tx
        print ("speed_tx :%sKb/s" % (speed_tx*8))
        return float(speed_tx*8)
    '''
    死循环打印当前的上行下行网速
    '''
    def get_network_speed_rx_tx(self,uid):
        while True:
            first_rx = self.get_rx(uid)
            first_tx = self.get_tx(uid)
            time.sleep(1)
            last_rx = self.get_rx(uid)
            last_tx = self.get_tx(uid)
            speed_rx = last_rx - first_rx
            speed_tx = last_tx - first_tx
            print ("speed_rx :%sKb/s;speed_tx :%sKb/s" % ((speed_rx * 8),(speed_tx*8)))
    '''
    求一段时间内的平均网速
    '''
    def get_average_speed_rx_tx(self,uid):
        num = 10
        speed_rx_total = 0
        speed_tx_total = 0
        for i in range(0,num):
            speed_rx = self.get_network_speed_rx(uid)
            speed_rx_total += speed_rx
            speed_tx = self.get_network_speed_tx(uid)
            speed_tx_total += speed_tx
        print ("average_speed_rx is:%.2fKb/s"%(speed_rx_total/num))
        print ("average_speed_tx is:%.2fKb/s"%(speed_tx_total/num))
import psutil,time,sys,logging,os

logName = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
path = os.getcwd()+"/"+logName+".txt"
handler = logging.FileHandler(path)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def getChromeCPU():
    webRTCCPU = 0
    chromePidlist = getChromePid()
    for pid in chromePidlist:
        pro = psutil.Process(int(pid))
        pro.cpu_percent(None)
        time.sleep(2)
        pCPU = pro.cpu_percent(None)
        print(pid ," pid CPU is ",pCPU)
        # logger.info(pid," CPU is ",pCPU)

        webRTCCPU += pCPU
    # print("******************* webRTC_CPU is %.2f%% *******************" %(webRTCCPU/2))
    return webRTCCPU/2

def getChromeMEM():
    webRTCMEM = 0
    chromePidlist = getChromePid()
    for pid in chromePidlist:
        time.sleep(2)
        virmem = psutil.virtual_memory()
        getMemP = psutil.Process(int(pid))
        Pmem = (getMemP.memory_percent() / 100) * virmem.used / 1024 / 1024
        print("pid:", pid + " mem is", Pmem)
        # logger.info("pid: ",pid + "mem is ", Pmem)
        webRTCMEM += Pmem
    # print("=================== webRTC_MEM is %.2fMB ===================" % webRTCMEM)
    return webRTCMEM

# def getMEM(GPUpid,Capturepid,premiumpid):
#     mem = psutil.virtual_memory()
#     GPUp = psutil.Process(GPUpid)
#     Capturep = psutil.Process(Capturepid)
#     premiump = psutil.Process(premiumpid)
#     GPUMEM = GPUp.memory_percent()
#     CaptureMEM = Capturep.memory_percent()
#     premiumMEM = premiump.memory_percent()
#     memUSED = mem.used
#     webRTCMEM = (((GPUMEM+CaptureMEM+premiumMEM)/100)*(memUSED))/1024/1024
#     print("GPU MEM is %dMB"% ((((GPUMEM)/100)*(memUSED))/1024/1024))
#     print("Capture MEM is %sMB"% ((((CaptureMEM)/100)*(memUSED))/1024/1024))
#     print("Premium MEM is %sMB"% ((((premiumMEM)/100)*(memUSED))/1024/1024))
#     logger.info("GPU MEM is %dMB"% ((((GPUMEM)/100)*(memUSED))/1024/1024))
#     logger.info("Capture MEM is %sMB"% ((((CaptureMEM)/100)*(memUSED))/1024/1024))
#     logger.info("Premium MEM is %sMB"% ((((premiumMEM)/100)*(memUSED))/1024/1024))
#     print("=================== webRTC_MEM is %.2fMB ===================" % webRTCMEM)
#     return webRTCMEM


def getSafariCPU():
    safariPidList = getsafariPid()
    webRTCCPU = 0
    for pid in safariPidList:
        pro = psutil.Process(int(pid))
        pro.cpu_percent(None)
        time.sleep(2)
        proCPU = pro.cpu_percent(None)
        print(pid," pid CPU is %d%%" % (proCPU))
        # logger.info(pid, " pid CPU is %d%%" % (proCPU))
        webRTCCPU += proCPU
        # print("******************* webRTC_CPU is %.2f%% *******************" % (webRTCCPU / 2))
    return webRTCCPU / 2

def getSafariMEM():
    webRTCMEM = 0
    safariPidlist = getsafariPid()
    for pid in safariPidlist:
        time.sleep(2)
        virmem = psutil.virtual_memory()
        getMemP = psutil.Process(int(pid))
        Pmem = (getMemP.memory_percent() / 100) * virmem.used / 1024 / 1024
        print("pid:", pid + " mem is", Pmem)
        # logger.info("pid: ",pid + "mem is ", Pmem)
        webRTCMEM += Pmem
    # print("=================== webRTC_MEM is %.2fMB ===================" % webRTCMEM)
    return webRTCMEM

def getChromeCPUMEM(secs,GPUpid, Capturepid, premiumpid):
    cpuTotal = 0
    memTotal = 0
    for i in range(0,10):
        time.sleep(secs)
        cpu = getCPU(GPUpid, Capturepid, premiumpid)
        print("*******************第%d组 webRTC_CPU is %.2f%% *******************" % ((i+1),cpu))
        logger.info("*******************第%d组 webRTC_CPU is %.2f%% *******************" % ((i+1),cpu))
        mem = getMEM(GPUpid, Capturepid, premiumpid)
        print("===================第%d组 webRTC_MEM is %.2fMB ===================" % ((i+1),mem))
        logger.info("===================第%d组 webRTC_MEM is %.2fMB ===================" % ((i+1),mem))
        cpuTotal += cpu
        memTotal += mem
    print("cpu平均值为：%.2f"%(cpuTotal/10))
    print("内存平均值为：%.2f"%(memTotal/10))
    logger.info("cpu平均值为：%.2f"%(cpuTotal/10))
    logger.info("内存平均值为：%.2f"%(memTotal/10))

def getChromeCPUMEM_autoGetPid(secs):
    cpuTotal = 0
    memTotal = 0
    for i in range(0,10):
        time.sleep(secs)
        cpu = getChromeCPU()
        print("*******************第%d组 webRTC_CPU is %.2f%% *******************" % ((i+1),cpu))
        logger.info("*******************第%d组 webRTC_CPU is %.2f%% *******************" % ((i+1),cpu))
        mem = getChromeMEM()
        print("===================第%d组 webRTC_MEM is %.2fMB ===================" % ((i+1),mem))
        logger.info("===================第%d组 webRTC_MEM is %.2fMB ===================" % ((i+1),mem))
        cpuTotal += cpu
        memTotal += mem
    print("cpu平均值为：%.2f"%(cpuTotal/10))
    print("内存平均值为：%.2f"%(memTotal/10))
    logger.info("cpu平均值为：%.2f"%(cpuTotal/10))
    logger.info("内存平均值为：%.2f"%(memTotal/10))

def getSafariCPUMEM_autoGetPid(secs):
    cpuTotal = 0
    memTotal = 0
    for i in range(0,10):
        time.sleep(secs)
        cpu = getSafariCPU()
        print("*******************第%d组 webRTC_CPU is %.2f%% *******************" % ((i+1),cpu))
        logger.info("*******************第%d组 webRTC_CPU is %.2f%% *******************" % ((i+1),cpu))
        mem = getSafariMEM()
        print("===================第%d组 webRTC_MEM is %.2fMB ===================" % ((i+1),mem))
        logger.info("===================第%d组 webRTC_MEM is %.2fMB ===================" % ((i+1),mem))
        cpuTotal += cpu
        memTotal += mem
    print("cpu平均值为：%.2f"%(cpuTotal/10))
    print("内存平均值为：%.2f"%(memTotal/10))
    logger.info("cpu平均值为：%.2f"%(cpuTotal/10))
    logger.info("内存平均值为：%.2f"%(memTotal/10))

def getSafariCPUMEM(secs,safariProcesspid,premiumpid):
    cpuTotal = 0
    memTotal = 0
    for i in range(0,10):
        time.sleep(secs)
        cpu = getSafariCPU(safariProcesspid,premiumpid)
        print("*******************第%d组 webRTC_CPU is %.2f%% *******************" % ((i+1),cpu))
        logger.info("*******************第%d组 webRTC_CPU is %.2f%% *******************" % ((i+1),cpu))
        mem = getSafariMEM(safariProcesspid,premiumpid)
        print("===================第%d组 webRTC_MEM is %.2fMB ===================" % ((i+1),mem))
        logger.info("===================第%d组 webRTC_MEM is %.2fMB ===================" % ((i+1),mem))
        cpuTotal += cpu
        memTotal += mem
    print("cpu平均值为：%.2f"%(cpuTotal/10))
    print("内存平均值为：%.2f"%(memTotal/10))
    logger.info("cpu平均值为：%.2f"%(cpuTotal/10))
    logger.info("内存平均值为：%.2f"%(memTotal/10))

def getChromePid():
    renderpidinfo = os.popen("ps -ef | grep 'Google Chrome.app' | grep 'type=renderer' | grep 'renderer-client-id=7'| awk '{print $2}'")
    renderpidlist = renderpidinfo.read().split("\n")[:-2]

    gpupidinfo = os.popen("ps -ef | grep 'Google Chrome.app' | grep 'gpu-preferences' | awk '{print $2}'")
    gpuuidlist = gpupidinfo.read().split("\n")[:-2]

    mediapidinfo = os.popen("ps -ef | grep 'Google Chrome.app' | grep 'type=utility' | grep 'message-loop-type-ui' | awk '{print $2}'")

    mediauidlist = mediapidinfo.read().split("\n")[:-2]

    chromepidlist = renderpidlist + gpuuidlist + mediauidlist
    print("chromePidList is :",chromepidlist)
    return chromepidlist

def getsafariPid():
    safaripidInfo = os.popen("ps -ef | grep 'Safari.app' | awk '{print $2}'")
    safaripidlist = safaripidInfo.read().split("\n")[:-3]

    premiumpidinfo = os.popen("ps -ef | grep 'XPCServices/com.apple.WebKit.WebContent.xpc' | awk '{print $2}'")
    premiumpidlist = premiumpidinfo.read().split("\n")[:-3]

    safaripidlist = safaripidlist + premiumpidlist
    print("safaripidlist is :",safaripidlist)
    return safaripidlist

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('''run as: python3 macBrowserCpuMem.py browserType secs 
                 browserType:chrome or safari
                 secs:sleep time
                ''')
        exit()
    browserType = sys.argv[1]
    if browserType == "chrome":
        secs = int(sys.argv[2])
        getChromeCPUMEM_autoGetPid(secs)
    elif browserType == "safari":
        secs = int(sys.argv[2])
        getSafariCPUMEM_autoGetPid(secs)


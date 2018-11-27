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

def getCPU(GPUpid,Capturepid,premiumpid):
    GPUp = psutil.Process(GPUpid)
    Capturep = psutil.Process(Capturepid)
    premiump = psutil.Process(premiumpid)
    GPUp.cpu_percent(None)
    time.sleep(2)
    GPUCPU = GPUp.cpu_percent(None)
    print("GPUCPU is %d%%"%(GPUCPU))
    logger.info("GPUCPU is %d%%"%(GPUCPU))
    Capturep.cpu_percent(None)
    time.sleep(2)
    CaptureCPU = Capturep.cpu_percent(None)
    print("CaptureCPU is %d%%" %(CaptureCPU))
    logger.info("CaptureCPU is %d%%" %(CaptureCPU))
    premiump.cpu_percent(None)
    time.sleep(2)
    premiumCPU = premiump.cpu_percent(None)
    print("premiumCPU is %d%%" %(premiumCPU))
    logger.info("premiumCPU is %d%%" %(premiumCPU))
    webRTCCPU = GPUCPU+CaptureCPU+premiumCPU
    print("******************* webRTC_CPU is %.2f%% *******************" %(webRTCCPU/2))
    return webRTCCPU/2

def getMEM(GPUpid,Capturepid,premiumpid):
    mem = psutil.virtual_memory()
    GPUp = psutil.Process(GPUpid)
    Capturep = psutil.Process(Capturepid)
    premiump = psutil.Process(premiumpid)
    GPUMEM = GPUp.memory_percent()
    CaptureMEM = Capturep.memory_percent()
    premiumMEM = premiump.memory_percent()
    memUSED = mem.used
    webRTCMEM = (((GPUMEM+CaptureMEM+premiumMEM)/100)*(memUSED))/1024/1024
    print("GPU MEM is %dMB"% ((((GPUMEM)/100)*(memUSED))/1024/1024))
    print("Capture MEM is %sMB"% ((((CaptureMEM)/100)*(memUSED))/1024/1024))
    print("Premium MEM is %sMB"% ((((premiumMEM)/100)*(memUSED))/1024/1024))
    logger.info("GPU MEM is %dMB"% ((((GPUMEM)/100)*(memUSED))/1024/1024))
    logger.info("Capture MEM is %sMB"% ((((CaptureMEM)/100)*(memUSED))/1024/1024))
    logger.info("Premium MEM is %sMB"% ((((premiumMEM)/100)*(memUSED))/1024/1024))
    print("=================== webRTC_MEM is %.2fMB ===================" % webRTCMEM)
    return webRTCMEM

def getSafariCPU(safariProcesspid,premiumpid):
    safarip = psutil.Process(safariProcesspid)
    premiump = psutil.Process(premiumpid)
    safarip.cpu_percent(None)
    time.sleep(2)
    safariProcessCPU = safarip.cpu_percent(None)
    print("safariProcess CPU is %d%%" % (safariProcessCPU))
    logger.info("safariProcess CPU is %d%%" % (safariProcessCPU))
    premiump.cpu_percent(None)
    time.sleep(2)
    premiumCPU = premiump.cpu_percent(None)
    print("premiumCPU is %d%%" % (premiumCPU))
    logger.info("premiumCPU is %d%%" % (premiumCPU))
    webRTCCPU = safariProcessCPU + premiumCPU
    print("******************* webRTC_CPU is %.2f%% *******************" % (webRTCCPU / 2))
    return webRTCCPU / 2

def getSafariMEM(safariProcesspid,premiumpid):
    mem = psutil.virtual_memory()
    memUSED = mem.used

    safariProcessp = psutil.Process(safariProcesspid)
    premiump = psutil.Process(premiumpid)

    safariProcessMEM = safariProcessp.memory_percent()
    premiumMEM = premiump.memory_percent()

    webRTCMEM = (((safariProcessMEM + premiumMEM) / 100) * (memUSED)) / 1024 / 1024
    print("safariProcess MEM is %dMB" % ((((safariProcessMEM) / 100) * (memUSED)) / 1024 / 1024))
    print("Premium MEM is %sMB" % ((((premiumMEM) / 100) * (memUSED)) / 1024 / 1024))
    logger.info("safariProcess MEM is %dMB" % ((((safariProcessMEM) / 100) * (memUSED)) / 1024 / 1024))
    logger.info("Premium MEM is %sMB" % ((((premiumMEM) / 100) * (memUSED)) / 1024 / 1024))
    print("=================== webRTC_MEM is %.2fMB ===================" % webRTCMEM)
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
        # print("===================第%d组 webRTC_MEM is %.2fMB ===================" % ((i+1),mem))
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

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print ('''run as: python3 macBrowserCpuMem.py browserType secs *pid
                browserType:chrome or safari
                secs:sleep time
                *pid:
                    chrome:GPUpid Capturepid premiumpid
                    safari:safariProcesspid premiumpid
               ''')
        exit(1)
    browserType = sys.argv[1]
    if browserType == "chrome":
        secs = int(sys.argv[2])
        GPUpid = int(sys.argv[3])
        Capturepid = int(sys.argv[4])
        premiumpid = int(sys.argv[5])
        getChromeCPUMEM(secs,GPUpid, Capturepid, premiumpid)
    elif browserType == "safari":
        secs = int(sys.argv[2])
        safariProcesspid = int(sys.argv[3])
        premiumpid = int(sys.argv[4])
        getSafariCPUMEM(secs, safariProcesspid, premiumpid)
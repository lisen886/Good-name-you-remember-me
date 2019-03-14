import psutil,time,sys,logging,os

logName = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
path = os.getcwd()+"/"+logName+".txt"
handler = logging.FileHandler(path)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(console)

def getCPU(GPUpid,Capturepid,premiumpid):
    GPUp = psutil.Process(GPUpid)
    Capturep = psutil.Process(Capturepid)
    premiump = psutil.Process(premiumpid)
    GPUp.cpu_percent(None)
    time.sleep(2)
    GPUCPU = GPUp.cpu_percent(None)
    logger.info("GPUCPU is %d%%"%(GPUCPU))
    Capturep.cpu_percent(None)
    time.sleep(2)
    CaptureCPU = Capturep.cpu_percent(None)
    logger.info("CaptureCPU is %d%%" %(CaptureCPU))
    premiump.cpu_percent(None)
    time.sleep(2)
    premiumCPU = premiump.cpu_percent(None)
    logger.info("premiumCPU is %d%%" %(premiumCPU))
    webRTCCPU = GPUCPU+CaptureCPU+premiumCPU
    return webRTCCPU/2,GPUCPU/2,CaptureCPU/2,premiumCPU/2

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
    GPUMEM = (((GPUMEM)/100)*(memUSED))/1024/1024
    CaptureMEM = (((CaptureMEM)/100)*(memUSED))/1024/1024
    premiumMEM = (((premiumMEM)/100)*(memUSED))/1024/1024
    logger.info("GPU MEM is %dMB"% GPUMEM)
    logger.info("Capture MEM is %sMB"% CaptureMEM)
    logger.info("Premium MEM is %sMB"% premiumMEM)
    return webRTCMEM,GPUMEM,CaptureMEM,premiumMEM

def getSafariCPU(safariProcesspid,premiumpid):
    safarip = psutil.Process(safariProcesspid)
    premiump = psutil.Process(premiumpid)
    safarip.cpu_percent(None)
    time.sleep(2)
    safariProcessCPU = safarip.cpu_percent(None)
    logger.info("safariProcess CPU is %d%%" % (safariProcessCPU))
    premiump.cpu_percent(None)
    time.sleep(2)
    premiumCPU = premiump.cpu_percent(None)
    logger.info("premiumCPU is %d%%" % (premiumCPU))
    webRTCCPU = safariProcessCPU + premiumCPU
    return webRTCCPU / 2,safariProcessCPU/2,premiumCPU/2

def getSafariMEM(safariProcesspid,premiumpid):
    mem = psutil.virtual_memory()
    memUSED = mem.used

    safariProcessp = psutil.Process(safariProcesspid)
    premiump = psutil.Process(premiumpid)

    safariProcessMEM = safariProcessp.memory_percent()
    premiumMEM = premiump.memory_percent()

    webRTCMEM = (((safariProcessMEM + premiumMEM) / 100) * (memUSED)) / 1024 / 1024
    safariProcessMEM = ((((safariProcessMEM) / 100) * (memUSED)) / 1024 / 1024)
    premiumMEM = ((((premiumMEM) / 100) * (memUSED)) / 1024 / 1024)
    logger.info("safariProcess MEM is %dMB" % safariProcessMEM)
    logger.info("Premium MEM is %sMB" % premiumMEM)
    return webRTCMEM,safariProcessMEM,premiumMEM

def getChromeCPUMEM(secs,frequency,GPUpid, Capturepid, premiumpid):
    cpuTotal = 0
    memTotal = 0
    GPUCPUTotal = 0
    CaptureCPUTotal = 0
    premiumCPUTotal = 0
    GPUMEMTotal = 0
    CaptureMEMTotal = 0
    premiumMEMTotal = 0
    for i in range(0,frequency):
        time.sleep(secs)
        webRTCCPU , GPUCPU, CaptureCPU, premiumCPU = getCPU(GPUpid, Capturepid, premiumpid)
        logger.info("*******************第%d组 webRTC_CPU is %.2f%% *******************" % ((i+1),webRTCCPU))
        webRTCMEM, GPUMEM, CaptureMEM, premiumMEM = getMEM(GPUpid, Capturepid, premiumpid)
        logger.info("===================第%d组 webRTC_MEM is %.2fMB ===================" % ((i+1),webRTCMEM))
        cpuTotal += webRTCCPU
        memTotal += webRTCMEM
        GPUCPUTotal += GPUCPU
        CaptureCPUTotal += CaptureCPU
        premiumCPUTotal += premiumCPU
        GPUMEMTotal += GPUMEM
        CaptureMEMTotal += CaptureMEM
        premiumMEMTotal += premiumMEM
    logger.info("GPUCPU平均值为：%.2f"%(GPUCPUTotal/frequency))
    logger.info("CaptureCPU平均值为：%.2f"%(CaptureCPUTotal/frequency))
    logger.info("premiumCPU平均值为：%.2f"%(premiumCPUTotal/frequency))
    logger.info("GPU内存平均值为：%.2f"%(GPUMEMTotal/frequency))
    logger.info("Capture内存平均值为：%.2f"%(CaptureMEMTotal/frequency))
    logger.info("premium内存平均值为：%.2f"%(premiumMEMTotal/frequency))
    logger.info("****************cpu平均值为：%.2f****************" % (cpuTotal / frequency))
    logger.info("****************内存平均值为：%.2f****************" % (memTotal / frequency))


def getSafariCPUMEM(secs,frequency,safariProcesspid,premiumpid):
    cpuTotal = 0
    memTotal = 0
    safariProcessCPUTotal = 0
    premiumCPUTotal = 0
    safariProcessMEMTotal = 0
    premiumMEMTotal = 0
    for i in range(0,frequency):
        time.sleep(secs)
        cpu,safariProcessCPU,premiumCPU = getSafariCPU(safariProcesspid,premiumpid)
        logger.info("*******************第%d组 webRTC_CPU is %.2f%% *******************" % ((i+1),cpu))
        mem,safariProcessMEM,premiumMEM = getSafariMEM(safariProcesspid,premiumpid)
        logger.info("===================第%d组 webRTC_MEM is %.2fMB ===================" % ((i+1),mem))
        cpuTotal += cpu
        memTotal += mem
        safariProcessCPUTotal += safariProcessCPU
        premiumCPUTotal += premiumCPU
        safariProcessMEMTotal += safariProcessMEM
        premiumMEMTotal += premiumMEM

    logger.info("safariProcessCPU平均值为：%.2f"%(safariProcessCPUTotal/frequency))
    logger.info("premiumCPU平均值为：%.2f"%(premiumCPUTotal/frequency))
    logger.info("safariProcess内存平均值为：%.2f"%(safariProcessMEMTotal/frequency))
    logger.info("premium内存平均值为：%.2f"%(premiumMEMTotal/frequency))
    logger.info("****************cpu平均值为：%.2f****************" % (cpuTotal / frequency))
    logger.info("****************内存平均值为：%.2f****************" % (memTotal / frequency))

if __name__ == '__main__':
    if len(sys.argv) < 5:
        logger.error (
            '''\nrun as: python3 macBrowserCpuMem.py browserType secs frequency *pid
                browserType:chrome or safari
                secs:sleep time
                frequency:run times
                *pid:
                    chrome:GPUpid Capturepid premiumpid
                    safari:safariProcesspid premiumpid
            ''')
        exit(1)
    browserType = sys.argv[1]
    if browserType == "chrome":
        secs = int(sys.argv[2])
        frequency = int(sys.argv[3])
        GPUpid = int(sys.argv[4])
        Capturepid = int(sys.argv[5])
        premiumpid = int(sys.argv[6])
        getChromeCPUMEM(secs,frequency, GPUpid, Capturepid, premiumpid)
    elif browserType == "safari":
        secs = int(sys.argv[2])
        frequency = int(sys.argv[3])
        safariProcesspid = int(sys.argv[4])
        premiumpid = int(sys.argv[5])
        getSafariCPUMEM(secs, frequency, safariProcesspid, premiumpid)
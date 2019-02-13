from bs4 import BeautifulSoup
import os

class execute():
    currentPath = os.path.abspath('.')
    reportPath = currentPath+"/report.html"
    def runFullTest(self,tag):
        if os.path.exists(self.currentPath):
            os.system("rm -r "+self.reportPath)
        cmd = "python3 -m pytest /Users/lisen/Desktop/premium_robot/webRtcGypsy/test_webRtcFullTest.py --tags "+tag+" --html="+self.reportPath
        os.system(cmd)
    def getFailCaseName(self):
        failCaseList = []
        file = open(self.reportPath, 'rb')
        html = file.read()
        x = BeautifulSoup(html,"html.parser")
        resultList = x.find_all('tbody', attrs={'class': 'failed results-table-row'})
        for i in range(0, len(resultList)):
            resultTag = resultList[i].find('td', attrs={'class': 'col-name'})
            cameName = resultTag.text.split("::")[-1]
            failCaseList.append(cameName)
        return failCaseList

    def runFailCase(self):
        failCases = self.getFailCaseName()
        if len(failCases) != 0:
            for case in failCases:
                cmd = "python3 -m pytest /Users/lisen/Desktop/premium_robot/webRtcGypsy/test_webRtcFullTest.py -v -k "+case+" --html=rerunReport.html"
                os.system(cmd)


    def pyrerun(self,tag,times):
        if os.path.exists(self.currentPath):
            os.system("rm -r "+self.reportPath)
        cmd= "python3 -m pytest /Users/lisen/Desktop/premium_robot/webRtcGypsy/test_webRtcFullTest.py --tags "+tag+" --html="+self.reportPath+" --reruns "+times
        os.system(cmd)
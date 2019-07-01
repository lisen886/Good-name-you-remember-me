import requests,json,os,sys,xlrd

class jiraApi():
    def __init__(self):
        # self.domainName = "jira.agora.io"
        self.domainName = input('Please enter the JIRA domain name(jira.ag**a.io):')
        userName = input('Please enter the JIRA account name:')
        passWord = input('Please enter the JIRA account password:')
        self.headers = {"Content-Type": "application/json; charset=UTF-8", }
        if self.getMyPermissions(userName, passWord) == False:
            passWord = input('Please enter the JIRA account password again:')
            if self.getMyPermissions(userName, passWord) == False:
                exit("密码错误")

    def getMyPermissions(self, userName, passWord):
        url = "https://" + self.domainName + "/rest/api/2/mypermissions"
        try:
            res = requests.get(url=url, auth=(userName, passWord)).json()
            self.auth = (userName, passWord)
            return True
        except:
            return False

    # 获取Jira自定义字段ID
    def getJiraFields(self):
        url = "https://"+self.domainName+"/rest/api/2/field"
        try:
            res = requests.get(url=url,auth=self.auth)
            print(res.text)
        except:
            print("get jira fields fail")

    # 新增测试用例
    def createTestCase(self,summary="",description="",priority="Medium",is_automated="No",product="None",labels=list(),osList=list(),testCaseModeList=list(),stepDictList=list()):
        url = "https://"+self.domainName+"/rest/api/2/issue"
        # customfield_12305:Test Type
        # customfield_10700:OS
        # customfield_12309:Manual Test Steps
        # customfield_12336:Is_automated--Yes/No
        # customfield_12337:Testcase模式
        # customfield_12335:Products:WebSDK/MainSDK/RecordingSDK
        # priority:Medium,High,Low
        testCaseJsonStr = {
            "fields": {
                "project": {"key": "TES"},
                "summary": summary,
                "description": description,
                "priority":{"name":priority},
                "issuetype": {"name": "Test"},
                "customfield_12305": {"value": "Manual"},
                "customfield_12335": {"value": product},
                "customfield_12336": {"value": is_automated}
            }
        }

        if isinstance(labels,list):
            testCaseJsonStr["fields"].update({"labels": labels})
        osJsonList = []
        if isinstance(osList, list) and len(osList) > 0:
            for os in osList:
                osJsonList.append({"value": os})
            testCaseJsonStr["fields"].update({"customfield_10700": osJsonList})
        testCaseModeJsonList = []
        if isinstance(testCaseModeList, list) and len(testCaseModeList) > 0:
            for testCaseMode in testCaseModeList:
                testCaseModeJsonList.append({"value": testCaseMode})
            testCaseJsonStr["fields"].update({"customfield_12337": testCaseModeJsonList})
        stepJsonList = []
        if isinstance(stepDictList, list):
            index = 0
            for stepDict in stepDictList:
                if isinstance(stepDict, dict):
                    stepJsonList.append({
                                "index": index,
                                "step": stepDict["step"],
                                "data": "",
                                "result": stepDict["result"]
                            })
                index += 1
            testCaseJsonStr["fields"].update({"customfield_12309": {"steps": stepJsonList}})
        try:
            response = requests.post(url, data=json.dumps(testCaseJsonStr), headers=self.headers,auth=self.auth).json()
            # print(response)
            return response.get("key")
        except:
            print("this testcase create fail %s "% testCaseJsonStr["fields"]["summary"])

    # 获取测试用例
    def getTestCaseByKey(self,key):
        url = "https://"+self.domainName+"/rest/raven/1.0/api/test?keys="+key
        try:
            res = requests.get(url=url,auth=self.auth).json()
            return res
        except:
            print("get testCase fail %s " % key)

    def getTestCaseNameByKey(self,key):
        info = self.getTestCaseByKey(key)
        link = info[0].get("self")
        res = requests.get(url=link, auth=self.auth).json()
        return res.get("fields").get("summary")

    def getTestCaseByFilter(self,filter):
        url = "https://"+self.domainName+"/rest/raven/1.0/api/test?"+filter
        try:
            res = requests.get(url=url,auth=self.auth).json()
            return res
        except:
            print("get testCase fail by %s" % filter)

    def getTestCaseNamesFromTESByFilter(self):
        print("正在获取TES Project下所有的TestCase,该过程可能需要5min")
        # filter = "jql=project%20%3D%20TES" # 所有case
        filter = "jql=project%20%3D%20TES%20AND%20issuetype%20%3D%20Test%20AND%20Is_automated%20%3D%20No%20AND%20reporter%20in%20(currentUser())"  # 当前用户创建的case
        caseNameList = []
        testCasesInfo = self.getTestCaseByFilter(filter)
        for testcase in testCasesInfo:
            name = self.getTestCaseNameByKey(testcase.get("key"))
            caseNameList.append(name)
            # print(name)
        print("获取TestCase结束，总共%s条case"%str(len(caseNameList)))
        return caseNameList

    def searchJira(self):
        url = "https://"+self.domainName+"/rest/api/2/search"
        payload = json.dumps({
            "jql": 'project = TES AND issuetype = "Test Set"',
            "maxResults": 100000,
            "fields": [
                "summary"
            ]
        })
        try:
            response = requests.post(url, data=payload, headers=self.headers,auth=self.auth).json()
            return response.get("issues")
        except:
            print("search jira fail")
    def getJiraNames(self):
        jiraNames = []
        jiras = self.searchJira()
        for jira in jiras:
            # jiraNames.append(jira.get("fields").get("summary"))
            jiraNames.append({"name":jira.get("fields").get("summary"),"key":jira.get("key")})
        return jiraNames

    # 获取测试套件(Feature)
    def getTestSetByKey(self,key):
        url = "https://"+self.domainName+"/rest/raven/1.0/api/testset/"+key+"/test"
        try:
            res = requests.get(url=url, auth=self.auth)
            print(res.text)
        except:
            print("get testSet fail %s " % key)

    # 创建测试套件 Test Plan/Test Execution/Test Set
    def createTestJira(self,summary,type):
        url = "https://"+self.domainName+"/rest/api/2/issue/"
        jiraNameDicts = self.getJiraNames()
        for jiraNameDict in jiraNameDicts:
            if summary == jiraNameDict.get("name"):
                key = jiraNameDict.get("key")
                return key
        else:
            payload = json.dumps({
            "fields": {
               "project":
               {
                  "key": "TES"
               },
               "summary": summary,
               "description": "",
               "issuetype": {
                  "name": type
               }
           }
        })
            try:
                response = requests.post(url, data=payload, headers=self.headers,auth=self.auth).json()
                # print(response)
                return response.get("key")
            except:
                print("create %s fail" % type)

    # 删除测试套件 Test Plan/Test Execution/Test Set/Tests
    def deleteTestJira(self, key):
        url = "https://"+self.domainName+"/rest/api/2/issue/"+key
        try:
            response = requests.delete(url=url,headers=self.headers, auth=self.auth).text
            print(response)
        except:
            print("delete %s fail" % type)

    # 添加用例到测试集合(功能文件夹)
    def addTestsToTestSet(self,testCaseList,testSetId):
        url = "https://"+self.domainName+"/rest/raven/1.0/api/testset/"+testSetId+"/test"
        if isinstance(testCaseList,list):
            caseJson = {"add":testCaseList}
            try:
                response = requests.post(url, data=json.dumps(caseJson), headers=self.headers, auth=self.auth).text
            except:
                print("add testcases to testSet fail")
        else:
            print("please input list")


    # 删除用例从测试集合(功能文件夹)
    def removeTestsFromTestSet(self,testCaseList,testSetId):
        url = "https://"+self.domainName+"/rest/raven/1.0/api/testset/"+testSetId+"/test"
        if isinstance(testCaseList, list):
            caseJson = {"remove": testCaseList}
            try:
                response = requests.post(url, data=json.dumps(caseJson), headers=self.headers,auth=self.auth).text
                print(response)
            except:
                print("remove testcases from testSet fail")
        else:
            print("please input list")

    def deleteTestCaseFromTestSet(self,testSetId,testCaseId):
        url = "https://"+self.domainName+"/rest/raven/1.0/api/testset/"+testSetId+"/test/"+testCaseId
        try:
            response = requests.delete(url, headers=self.headers,auth=self.auth).text
            print(response)
        except:
            print("delete testCase from testSet fail")

    # 添加用例到测试执行(理解成不同的执行平台)
    def addTestSetOrTestCaseToTestExecution(self,testCaseOrSetList,testExecutionId):
        url = "https://"+self.domainName+"/rest/raven/1.0/api/testexec/" + testExecutionId + "/test"
        if isinstance(testCaseOrSetList, list):
            caseJson = {"add": testCaseOrSetList}
            try:
                response = requests.post(url, data=json.dumps(caseJson), headers=self.headers,auth=self.auth).text
                print(response)
            except:
                print("add testCaseOrSetList to testExecution fail")
        else:
            print("please input list")

    # 删除用例从测试执行中(理解成不同的执行平台)
    def removeTestSetOrTestCaseFromTestExecution(self,testCaseOrSetList,testExecutionId):
        url = "https://"+self.domainName+"/rest/raven/1.0/api/testexec/" + testExecutionId + "/test"
        if isinstance(testCaseOrSetList, list):
            caseJson = {"remove": testCaseOrSetList}
            try:
                response = requests.post(url, data=json.dumps(caseJson), headers=self.headers,auth=self.auth).text
                print(response)
            except:
                print("remove testCaseOrSetList from testExecution fail")
        else:
            print("please input list")

    def deleteTestCaseFromTestExecution(self,testExecutionId,testCaseId):
        url = "https://"+self.domainName+"/rest/raven/1.0/api/testexec/" + testExecutionId + "/test/"+testCaseId
        try:
            response = requests.delete(url, headers=self.headers,auth=self.auth).text
            print(response)
        except:
            print("delete testCase from testExecution fail")

    # 添加execution到测试plan
    def addTestExecutionToPlan(self,testExecutionList,testPlanId):
        url = "https://"+self.domainName+"/rest/raven/1.0/api/testplan/" + testPlanId + "/testexecution"
        if isinstance(testExecutionList, list):
            caseJson = {"add": testExecutionList}
            try:
                response = requests.post(url, data=json.dumps(caseJson), headers=self.headers,auth=self.auth).text
                print(response)
            except:
                print("add testExecutionList to testPlan fail")
        else:
            print("please input list")

    # 删除execution从plan中
    def removeTestExecutionFromPlan(self,testExecutionList,testPlanId):
        url = "https://"+self.domainName+"/rest/raven/1.0/api/testplan/" + testPlanId + "/testexecution"
        if isinstance(testExecutionList, list):
            caseJson = {"remove": testExecutionList}
            try:
                response = requests.post(url, data=json.dumps(caseJson), headers=self.headers, auth=self.auth).text
                print(response)
            except:
                print("remove testExecutionList from testPlan fail")
        else:
            print("please input list")

    def getTestPlanResult(self,testPlanKey):
        url = "https://" + self.domainName + "/rest/raven/1.0/testruns?testPlanKey=" + testPlanKey
        try:
            response = requests.get(url, headers=self.headers, auth=self.auth).json()
            return response
        except:
            print("get testplan result fail")

    def getTestPlanProgress(self,testPlanKey):
        reslist = self.getTestPlanResult(testPlanKey)
        count = 0
        passCount = 0
        failCount = 0
        todoCount = 0
        for res in reslist:
            status = res.get("status")
            if status != "TODO":
                count += 1
                if status == "PASS":
                    passCount += 1
                elif status == "FAIL":
                    failCount += 1
            elif status == "TODO":
                todoCount += 1
        rate = count / len(reslist)
        passRate = passCount / len(reslist)
        failRate = failCount / len(reslist)
        todoRate = todoCount / len (reslist)
        print("caseTotal:%d,execRate:%.2f,passRate:%.2f,failRate:%.2f,todoRate::%.2f" % (len(reslist),rate,passRate,failRate,todoRate))

class ProgressBar:
    def __init__(self, count = 0, total = 0, width = 50):
        self.count = count
        self.total = total
        self.width = width
    def move(self):
        self.count += 1
    def log(self, s):
        sys.stdout.write(' ' * (self.width + 9) + '\r')
        sys.stdout.flush()
        print(s)
        progress = self.width * self.count / self.total
        sys.stdout.write('{0:3}/{1:3}: '.format(self.count, self.total))
        sys.stdout.write('#' * int(progress) + '-' * (self.width - int(progress)) + '\r')
        if progress == self.width:
            sys.stdout.write('\n')
        sys.stdout.flush()

class excel2jira():

    def __init__(self):
        self.jira = jiraApi()
        self.checkJiraExistFlag = input('Check if the adding case exists(Y/N):')
        if self.checkJiraExistFlag in ["Y", "y", "Yes", "yes", "YES"]:
            self.caseNameList = self.jira.getTestCaseNamesFromTESByFilter()
        else:
            self.caseNameList = []

    def get_excelfile(self,path):
        L = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if os.path.splitext(file)[1] == '.xlsx':
                    L.append(path + '/' + file)
            if len(L) == 0:
                print('\033[1;31m %s\n %s\nThere is no Excel file,Please check out!\n %s' % (('*' * 50), path, ('*' * 50)))
            return L

    def import2jira(self,file):
        importanceDict = {
            "低": "Low",
            "中": "Medium",
            "高": "High"
        }
        workbook = xlrd.open_workbook(file)
        sheet = workbook.sheet_by_index(0)
        test_set = sheet.row_values(0)[0]
        case_count = sheet.nrows -2
        bar = ProgressBar(total=case_count)
        caseJiraIDLists = []
        for i in range(2, sheet.nrows):
            case_name = sheet.cell_value(i, 0)
            import time
            time.sleep(1)
            description = sheet.cell_value(i, 1)
            steps = sheet.cell_value(i, 2)
            expect_results = sheet.cell_value(i, 3)
            importance = importanceDict[str(sheet.cell_value(i, 4)).strip()]
            keywords = sheet.cell_value(i, 5).split("\n")
            os = sheet.cell_value(i, 6).split("\n")
            product = sheet.cell_value(i, 7).strip()
            is_automated = sheet.cell_value(i, 8).strip()
            testCaseModes = sheet.cell_value(i, 9).split("\n")
            stepDictList = []
            if "\n" not in steps:
                # 一个步骤多个结果，所有步骤和结果只放在一个step和result
                stepDictList.append({"step": steps, "result": expect_results})
            else:
                stepList = steps.split("\n")
                expectResultList = expect_results.split("\n")
                if len(stepList) != len(expectResultList):
                    # 多个步骤一个结果，所有的结果放在最后一个步骤中
                    for stepi in range(0, len(stepList)):
                        if stepi != len(stepList)-1:
                            stepDictList.append({"step": stepList[stepi], "result": ""})
                        else:
                            stepDictList.append({"step": stepList[stepi], "result": expect_results})
                else:
                    # 步骤和实际一一对应
                    for stepi in range(0, len(stepList)):
                        stepDictList.append({"step": stepList[stepi], "result": expectResultList[stepi]})
            if case_name not in self.caseNameList:
                case_jira_id = self.jira.createTestCase(summary=case_name,
                                                      description=description,
                                                      priority=importance,
                                                      is_automated=is_automated,
                                                      product=product,
                                                      labels=keywords,
                                                      osList=os,
                                                      testCaseModeList=testCaseModes,
                                                      stepDictList=stepDictList
                                                      )
                caseJiraIDLists.append(case_jira_id)
                bar.move()
                bar.log("Case created: %s | jira ID: %s" % (case_name,case_jira_id))
        if len(caseJiraIDLists) != 0:
            testSetJiraID = self.jira.createTestJira(test_set, "Test Set")
            print("Add the case of this list:%s to testSet:%s"%(caseJiraIDLists, testSetJiraID))
            self.jira.addTestsToTestSet(caseJiraIDLists, testSetJiraID)

if __name__ == '__main__':
    path = os.getcwd()  # for windows or pycharm
    # path = os.path.dirname(sys.executable)  # for mac
    e2j = excel2jira()
    file = e2j.get_excelfile(path)
    if len(file) != 0:
        e2j.import2jira(file[0])
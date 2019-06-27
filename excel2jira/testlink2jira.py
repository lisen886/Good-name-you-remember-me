import requests,json,testlink,re
from pyquery import PyQuery as pq
# pip install TestLink-API-Python-client
# pip install pyquery

class jiraApi():
    def __init__(self):
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
        if isinstance(osList, list) and len(osList)>0:
            for os in osList:
                osJsonList.append({"value": os})
            testCaseJsonStr["fields"].update({"customfield_10700": osJsonList})
        testCaseModeJsonList = []
        if isinstance(testCaseModeList, list):
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
            print(response)
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
        print("正在获取TES Project下所有的TestCase")
        # filter = "jql=project%20%3D%20TES"
        filter = "jql=project%20%3D%20TES%20AND%20issuetype%20%3D%20Test%20AND%20Is_automated%20%3D%20No%20AND%20reporter%20in%20(currentUser())"
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
                print(response)
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
                print(response)
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

class testLinkAPI():
    def __init__(self):
        self.url = 'http://10.80.0.220/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
        self.key = '*****************'  #自己去testlink中获取个人密钥
        self.tlc = testlink.TestlinkAPIClient(self.url, self.key)
        self.jira = jiraApi()
        self.caseNameList = self.jira.getTestCaseNamesFromTESByFilter()

    def get_testCases_sendTo_jira(self,test_project_name,keywords,product,osList,testCaseModeList,specifiedSuite=""):
        projectID = self.tlc.getProjectIDByName(test_project_name)
        project_prefix=self.get_project_prefix(test_project_name)
        caseCount= 0
        testSuites = self.tlc.getFirstLevelTestSuitesForTestProject(projectID)
        for suite in testSuites:
            suiteName = suite.get("name")
            if suiteName == specifiedSuite:
                try:
                    caseLists = []
                    testcasesInfo = self.tlc.getTestCasesForTestSuite(suite.get("id"), False, 'full')
                    for testcaseInfo in testcasesInfo:
                        caseid = project_prefix + "-" + testcaseInfo.get("tc_external_id")
                        caseInfo = self.get_test_case_info(caseid)
                        if caseInfo:
                            labels = []
                            for keyword in keywords:
                                if keyword in caseInfo[4]:
                                    keyword = keyword.replace(" ", "")
                                    labels.append(keyword)
                            if len(labels) != 0:
                                caseCount += 1
                                print(caseInfo)
                                if caseInfo[3] != "Yes":
                                    if caseInfo[0] not in self.caseNameList:
                                        caseJiraID = self.jira.createTestCase(summary=caseInfo[0],
                                                                              description=caseInfo[1],
                                                                              priority=caseInfo[2],
                                                                              is_automated=caseInfo[3],
                                                                              product=product,
                                                                              labels=labels,
                                                                              osList=osList,
                                                                              testCaseModeList=testCaseModeList,
                                                                              stepDictList=caseInfo[5])
                                        caseLists.append(caseJiraID)
                            # print(labels)
                    if len(caseLists) != 0:
                        print(suiteName)
                        setJiraID = self.jira.createTestJira(suiteName, "Test Set")
                        self.jira.addTestsToTestSet(caseLists, setJiraID)
                except:
                    print("**********************this %s is fail **********************" % testcaseInfo)

                childSuites = self.tlc.getTestSuitesForTestSuite(suite.get("id"))
                for childSuite in childSuites:
                    childCaseLists = []
                    suiteName = suite.get("name") + "-" + childSuites[childSuite]["name"]
                    testcasesInfo = self.tlc.getTestCasesForTestSuite(childSuite, True, 'simple')
                    for testcaseInfo in testcasesInfo:
                        caseid = testcaseInfo.get("external_id")
                        caseInfo = self.get_test_case_info(caseid)
                        if caseInfo:
                            labels = []
                            for keyword in keywords:
                                if keyword in caseInfo[4]:
                                    keyword = keyword.replace(" ", "")
                                    labels.append(keyword)
                            if len(labels) != 0:
                                caseCount += 1
                                print(caseInfo)
                                if caseInfo[3] != "Yes":
                                    if caseInfo[0] not in self.caseNameList:
                                        caseJiraID = self.jira.createTestCase(summary=caseInfo[0],
                                                                             description=caseInfo[1],
                                                                             priority=caseInfo[2],
                                                                             is_automated=caseInfo[3],
                                                                             product=product,
                                                                             labels=labels,
                                                                             osList=osList,
                                                                             testCaseModeList=testCaseModeList,
                                                                             stepDictList=caseInfo[5])
                                        childCaseLists.append(caseJiraID)
                            # print(labels)
                    if len(childCaseLists) != 0:
                        print(suiteName)
                        childsetJiraID = self.jira.createTestJira(suiteName, "Test Set")
                        self.jira.addTestsToTestSet(childCaseLists, childsetJiraID)
            elif specifiedSuite == "":
                # suiteName = suite.get("name")
                try:
                    caseLists = []
                    testcasesInfo = self.tlc.getTestCasesForTestSuite(suite.get("id"), False, 'full')
                    for testcaseInfo in testcasesInfo:
                        caseid = project_prefix + "-" + testcaseInfo.get("tc_external_id")
                        caseInfo = self.get_test_case_info(caseid)
                        if caseInfo:
                            labels = []
                            for keyword in keywords:
                                if keyword in caseInfo[4]:
                                    keyword = keyword.replace(" ", "")
                                    labels.append(keyword)
                            if len(labels) != 0:
                                caseCount += 1
                                print(caseInfo)
                                if caseInfo[3] != "Yes":
                                    if caseInfo[0] not in self.caseNameList:
                                        caseJiraID = self.jira.createTestCase(summary=caseInfo[0],
                                                                              description=caseInfo[1],
                                                                              priority=caseInfo[2],
                                                                              is_automated=caseInfo[3],
                                                                              product=product,
                                                                              labels=labels,
                                                                              osList=osList,
                                                                              testCaseModeList=testCaseModeList,
                                                                              stepDictList=caseInfo[5])
                                        caseLists.append(caseJiraID)
                            # print(labels)
                    if len(caseLists) != 0:
                        print(suiteName)
                        setJiraID = self.jira.createTestJira(suiteName, "Test Set")
                        self.jira.addTestsToTestSet(caseLists, setJiraID)
                except:
                    print("**********************this %s is fail **********************" % testcaseInfo)

                childSuites = self.tlc.getTestSuitesForTestSuite(suite.get("id"))
                for childSuite in childSuites:
                    childCaseLists = []
                    suiteName = suite.get("name") + "-" + childSuites[childSuite]["name"]
                    testcasesInfo = self.tlc.getTestCasesForTestSuite(childSuite, True, 'simple')
                    for testcaseInfo in testcasesInfo:
                        caseid = testcaseInfo.get("external_id")
                        caseInfo = self.get_test_case_info(caseid)
                        if caseInfo:
                            labels = []
                            for keyword in keywords:
                                if keyword in caseInfo[4]:
                                    keyword = keyword.replace(" ", "")
                                    labels.append(keyword)
                            if len(labels) != 0:
                                caseCount += 1
                                print(caseInfo)
                                if caseInfo[3] != "Yes":
                                    if caseInfo[0] not in self.caseNameList:
                                        caseJiraID = self.jira.createTestCase(summary=caseInfo[0],
                                                                              description=caseInfo[1],
                                                                              priority=caseInfo[2],
                                                                              is_automated=caseInfo[3],
                                                                              product=product,
                                                                              labels=labels,
                                                                              osList=osList,
                                                                              testCaseModeList=testCaseModeList,
                                                                              stepDictList=caseInfo[5])
                                        childCaseLists.append(caseJiraID)
                            # print(labels)
                    if len(childCaseLists) != 0:
                        print(suiteName)
                        childsetJiraID = self.jira.createTestJira(suiteName, "Test Set")
                        self.jira.addTestsToTestSet(childCaseLists, childsetJiraID)
            else:
                pass
        print(caseCount)

    def get_autotestCases_sendTo_jira(self,test_project_name,keywords,product,osList,testCaseModeList):
        projectID = self.tlc.getProjectIDByName(test_project_name)
        project_prefix=self.get_project_prefix(test_project_name)
        testSuites = self.tlc.getFirstLevelTestSuitesForTestProject(projectID)
        caseLists = []
        for suite in testSuites:
            try:
                testcasesInfo = self.tlc.getTestCasesForTestSuite(suite.get("id"), False, 'full')
                for testcaseInfo in testcasesInfo:
                    caseid = project_prefix + "-" + testcaseInfo.get("tc_external_id")
                    caseInfo = self.get_test_case_info(caseid)
                    if caseInfo:
                        labels = []
                        for keyword in keywords:
                            if keyword in caseInfo[4]:
                                keyword = keyword.replace(" ", "")
                                labels.append(keyword)
                        if len(labels) != 0:
                            print(caseInfo)
                            if caseInfo[3] == "Yes":
                                if caseInfo[0] not in self.caseNameList:
                                    caseJiraID = self.jira.createTestCase(summary=caseInfo[0],
                                                                          description=caseInfo[1],
                                                                          priority=caseInfo[2],
                                                                          is_automated=caseInfo[3],
                                                                          product=product,
                                                                          labels=labels,
                                                                          osList=osList,
                                                                          testCaseModeList=testCaseModeList,
                                                                          stepDictList=caseInfo[5])
                                    caseLists.append(caseJiraID)

            except:
                print("**********************this %s is fail **********************" % testcaseInfo)

            childSuites = self.tlc.getTestSuitesForTestSuite(suite.get("id"))
            for childSuite in childSuites:
                testcasesInfo = self.tlc.getTestCasesForTestSuite(childSuite, True, 'simple')
                for testcaseInfo in testcasesInfo:
                    caseid = testcaseInfo.get("external_id")
                    caseInfo = self.get_test_case_info(caseid)
                    if caseInfo:
                        labels = []
                        for keyword in keywords:
                            if keyword in caseInfo[4]:
                                keyword = keyword.replace(" ", "")
                                labels.append(keyword)
                        if len(labels) != 0:
                            print(caseInfo)
                            if caseInfo[3] == "Yes":
                                if caseInfo[0] not in self.caseNameList:
                                    caseJiraID = self.jira.createTestCase(summary=caseInfo[0],
                                                                          description=caseInfo[1],
                                                                          priority=caseInfo[2],
                                                                          is_automated=caseInfo[3],
                                                                          product=product,
                                                                          labels=labels,
                                                                          osList=osList,
                                                                          testCaseModeList=testCaseModeList,
                                                                          stepDictList=caseInfo[5])
                                    caseLists.append(caseJiraID)
        if len(caseLists) != 0:
            suiteName = "AUTO TEST CASE"
            JiraID = self.jira.createTestJira(suiteName, "Test Set")
            self.jira.addTestsToTestSet(caseLists, JiraID)

    def get_alltestCases_sendTo_jira(self,test_project_name,keywords,product,osList,testCaseModeList,specifiedSuite=""):
        projectID = self.tlc.getProjectIDByName(test_project_name)
        project_prefix=self.get_project_prefix(test_project_name)
        caseCount= 0
        testSuites = self.tlc.getFirstLevelTestSuitesForTestProject(projectID)
        for suite in testSuites:
            suiteName = suite.get("name")
            if suiteName == specifiedSuite:
                try:
                    caseLists = []
                    testcasesInfo = self.tlc.getTestCasesForTestSuite(suite.get("id"), False, 'full')
                    for testcaseInfo in testcasesInfo:
                        caseid = project_prefix + "-" + testcaseInfo.get("tc_external_id")
                        caseInfo = self.get_test_case_info(caseid)
                        if caseInfo:
                            labels = []
                            for keyword in keywords:
                                if keyword in caseInfo[4]:
                                    keyword = keyword.replace(" ", "")
                                    labels.append(keyword)
                            if len(labels) != 0:
                                caseCount += 1
                                print(caseInfo)
                                if caseInfo[0] not in self.caseNameList:
                                    caseJiraID = self.jira.createTestCase(summary=caseInfo[0],
                                                                          description=caseInfo[1],
                                                                          priority=caseInfo[2],
                                                                          is_automated=caseInfo[3],
                                                                          product=product,
                                                                          labels=labels,
                                                                          osList=osList,
                                                                          testCaseModeList=testCaseModeList,
                                                                          stepDictList=caseInfo[5])
                                    caseLists.append(caseJiraID)
                            # print(labels)
                    if len(caseLists) != 0:
                        print(suiteName)
                        setJiraID = self.jira.createTestJira(suiteName, "Test Set")
                        self.jira.addTestsToTestSet(caseLists, setJiraID)
                except:
                    print("**********************this %s is fail **********************" % testcaseInfo)

                childSuites = self.tlc.getTestSuitesForTestSuite(suite.get("id"))
                for childSuite in childSuites:
                    childCaseLists = []
                    suiteName = suite.get("name") + "-" + childSuites[childSuite]["name"]
                    testcasesInfo = self.tlc.getTestCasesForTestSuite(childSuite, True, 'simple')
                    for testcaseInfo in testcasesInfo:
                        caseid = testcaseInfo.get("external_id")
                        caseInfo = self.get_test_case_info(caseid)
                        if caseInfo:
                            labels = []
                            for keyword in keywords:
                                if keyword in caseInfo[4]:
                                    keyword = keyword.replace(" ","")
                                    labels.append(keyword)
                            if len(labels) != 0:
                                caseCount += 1
                                print(caseInfo)
                                if caseInfo[0] not in self.caseNameList:
                                    caseJiraID = self.jira.createTestCase(summary=caseInfo[0],
                                                                          description=caseInfo[1],
                                                                          priority=caseInfo[2],
                                                                          is_automated=caseInfo[3],
                                                                          product=product,
                                                                          labels=labels,
                                                                          osList=osList,
                                                                          testCaseModeList=testCaseModeList,
                                                                          stepDictList=caseInfo[5])
                                    childCaseLists.append(caseJiraID)
                            # print(labels)
                    if len(childCaseLists) != 0:
                        print(suiteName)
                        childsetJiraID = self.jira.createTestJira(suiteName, "Test Set")
                        self.jira.addTestsToTestSet(childCaseLists, childsetJiraID)
            elif specifiedSuite == "":
                # suiteName = suite.get("name")
                try:
                    caseLists = []
                    testcasesInfo = self.tlc.getTestCasesForTestSuite(suite.get("id"), False, 'full')
                    for testcaseInfo in testcasesInfo:
                        caseid = project_prefix + "-" + testcaseInfo.get("tc_external_id")
                        caseInfo = self.get_test_case_info(caseid)
                        if caseInfo:
                            labels = []
                            for keyword in keywords:
                                if keyword in caseInfo[4]:
                                    keyword = keyword.replace(" ", "")
                                    labels.append(keyword)
                            if len(labels) != 0:
                                caseCount += 1
                                print(caseInfo)
                                if caseInfo[0] not in self.caseNameList:
                                    caseJiraID = self.jira.createTestCase(summary=caseInfo[0],
                                                                          description=caseInfo[1],
                                                                          priority=caseInfo[2],
                                                                          is_automated=caseInfo[3],
                                                                          product=product,
                                                                          labels=labels,
                                                                          osList=osList,
                                                                          testCaseModeList=testCaseModeList,
                                                                          stepDictList=caseInfo[5])
                                    caseLists.append(caseJiraID)
                            # print(labels)
                    if len(caseLists) != 0:
                        print(suiteName)
                        setJiraID = self.jira.createTestJira(suiteName, "Test Set")
                        self.jira.addTestsToTestSet(caseLists, setJiraID)
                except:
                    print("**********************this %s is fail **********************" % testcaseInfo)

                childSuites = self.tlc.getTestSuitesForTestSuite(suite.get("id"))
                for childSuite in childSuites:
                    childCaseLists = []
                    suiteName = suite.get("name") + "-" + childSuites[childSuite]["name"]
                    testcasesInfo = self.tlc.getTestCasesForTestSuite(childSuite, True, 'simple')
                    for testcaseInfo in testcasesInfo:
                        caseid = testcaseInfo.get("external_id")
                        caseInfo = self.get_test_case_info(caseid)
                        if caseInfo:
                            labels = []
                            for keyword in keywords:
                                if keyword in caseInfo[4]:
                                    keyword = keyword.replace(" ", "")
                                    labels.append(keyword)
                            if len(labels) != 0:
                                caseCount += 1
                                print(caseInfo)
                                if caseInfo[0] not in self.caseNameList:
                                    caseJiraID = self.jira.createTestCase(summary=caseInfo[0],
                                                                          description=caseInfo[1],
                                                                          priority=caseInfo[2],
                                                                          is_automated=caseInfo[3],
                                                                          product=product,
                                                                          labels=labels,
                                                                          osList=osList,
                                                                          testCaseModeList=testCaseModeList,
                                                                          stepDictList=caseInfo[5])
                                    childCaseLists.append(caseJiraID)
                            # print(labels)
                    if len(childCaseLists) != 0:
                        print(suiteName)
                        childsetJiraID = self.jira.createTestJira(suiteName, "Test Set")
                        self.jira.addTestsToTestSet(childCaseLists, childsetJiraID)
            else:
                pass
        print(caseCount)

    def get_project_prefix(self,projectName):
        projects = self.tlc.getProjects()
        for project in projects:
            if project.get("name") == projectName:
                return project.get("prefix")

    def get_test_case_info(self,test_case_id):
        stepDictList = []
        status = ""
        test_case = ""
        re_h = re.compile('</?\w+[^>]*>')
        try:
            test_case = self.tlc.getTestCase(testcaseexternalid=test_case_id)[0]
            status = test_case.get("status")  # 7:Final
        except:
            print("##################### get this testcase info %s fail #####################"% test_case_id)
        if status != "7":
            return False
        keyWords = []
        kwDict = self.tlc.getTestCaseKeywords(testcaseexternalid=test_case_id)
        for kw in kwDict:
            keyWords.append(kwDict[kw])
        caseName = test_case.get("name")
        preconditions = test_case.get("preconditions")
        tagStr = re.match(re_h, preconditions)
        if str(tagStr) != "None":
            tag = str(tagStr.group(0))[1:-1]
            try:
                description = pq(preconditions)(tag).text()
            except:
                description = preconditions
        else:
            description = preconditions
        importance = test_case.get("importance")  # 3、2、1 ：高、中、低
        priority = ""
        if importance == "3":
            priority = "High"
        elif importance == "2":
            priority = "Medium"
        elif importance == "1":
            priority = "Low"
        is_automated = ""
        execution_type = test_case.get("execution_type")  # 1、2：手工、自动
        if execution_type == "1":
            is_automated = "No"
        elif execution_type == "2":
            is_automated = "Yes"
        for m in test_case.get("steps"):
            action = m.get("actions")
            result = m.get("expected_results")
            actionTagStr = re.match(re_h, action)
            if str(actionTagStr) != "None":
                tag = str(actionTagStr.group(0))[1:-1]
                try:
                    actionStr = pq(action)(tag).text()
                except:
                    actionStr = action

            else:
                actionStr = action

            if result != "":
                resultTagStr = re.match(re_h, result)
                if str(resultTagStr) != "None":
                    etag = str(resultTagStr.group(0))[1:-1]
                    try:
                        expectedStr = pq(result)(etag).text()
                    except:
                        expectedStr = result
                else:
                    expectedStr = result
            else:
                expectedStr = ""

            stepDictList.append({"step": actionStr, "result": expectedStr})


        return caseName,description,priority,is_automated,keyWords,stepDictList

# t = testLinkAPI()
# print(t.get_test_case_info("Live-3145"))
# t.get_testCases_sendTo_jira('Live_Broadcast',["web_H264","web_VP8"],"WebSDK",["Web"],["直播", "通信"],"WebRTC")
# t.get_autotestCases_sendTo_jira('Live_Broadcast',["web_H264","web_VP8"],"WebSDK",["Web"],["直播", "通信"])

# j = jiraApi()
# j.createTestCase(summary="用例标题",
#                  description="用例描述",
#                  priority="Medium",
#                  is_automated="No",
#                  product="WebSDK",
#                  labels=["web_H264"],
#                  osList=["Web"],
#                  testCaseModeList=["直播","通信"],
#                  stepDictList=[{"step":"第一步","result":"第一步结果"},{"step":"第二步","result":"第二步结果"}])
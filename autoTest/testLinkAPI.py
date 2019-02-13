import testlink,sys,time

url = 'http://qa.agoralab.co/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
key = '83301958459ed090e8cf01f4d1832bce'
tlc = testlink.TestlinkAPIClient(url, key)

def get_testcaseid_testPlanid_buildname(TestCaseID,test_plan_name):
    case_id = ""
    test_project_name = 'Live_Broadcast'
    # test_plan_name = "Web_Live_H264_mv2.5.1_battest"
    test_plan = tlc.getTestPlanByName(test_project_name, test_plan_name)
    tps = tlc.getProjectTestPlans(test_plan[0]["testproject_id"])
    test_plan_id = test_plan[0]['id']
    response = tlc.getBuildsForTestPlan(test_plan_id)
    build_name = response[0]['name']
    for tp in tps:
        if tp["name"] == test_plan_name:
            cases = tlc.getTestCasesForTestPlan(tp["id"])
            if isinstance(cases, dict):
                for key in cases:
                    if isinstance(cases[key], dict):
                        for key2 in cases[key]:
                            if cases[key][key2]["full_external_id"] == TestCaseID:
                                case_id = cases[key][key2]["tcase_id"]
    return case_id,test_plan_id,build_name

def set_result(test_plan_name,platformName,testResult,testCaseID):
    case_id, test_plan_id, build_name = get_testcaseid_testPlanid_buildname(testCaseID,test_plan_name)
    tlc.reportTCResult(testcaseid=case_id, testplanid=test_plan_id, buildname=build_name,
                       status=testResult, notes='', platformname=platformName)

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
if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('''\nrun as: python3 testLinkAPI.py test_plan_name platformName testResult *testCaseID
               test_plan_name: "Web_Live_H264_mv2.5.1_battest"
               platformName: "Chrome on Mac"
               testResult: "p" or "f"
               *testCaseID: "Live-001" "Live-002"

               eg:python3 autoTest/testLinkAPI.py "Web_Live_H264_mv2.5.1_battest" "Chrome on Mac" "p" "Live-882" "Live-883"
        ''')
        exit(1)
    test_plan_name = sys.argv[1]
    platformName = sys.argv[2]
    testResult = sys.argv[3]
    testCaseIDs = sys.argv[4:]
    bar = ProgressBar(total=len(testCaseIDs))
    for testCaseID in testCaseIDs:
        bar.move()
        bar.log('%s is playing the result'%testCaseID)
        set_result(test_plan_name,platformName,testResult,testCaseID)
import testlink,json,sys
url = 'http://qa.agoralab.co/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
key = '83301958459ed090e8cf01f4d1832bce'
tlc = testlink.TestlinkAPIClient(url, key)
# tlc.listProjects()

def get_testcasenumber(dic_json):
    casenum = 0
    all_pass = 0
    all_fail = 0
    all_block = 0
    all_no_run = 0
    if isinstance(dic_json, dict):
        for key in dic_json:
            if isinstance(dic_json[key], dict):
                casenum += len(dic_json[key])
                for key2 in dic_json[key]:
                    if dic_json[key][key2]["exec_status"] == "p":
                        all_pass += 1
                    elif dic_json[key][key2]["exec_status"] == "f":
                        all_fail += 1
                    elif dic_json[key][key2]["exec_status"] == "b":
                        all_block += 1
                    elif dic_json[key][key2]["exec_status"] == "n":
                        all_no_run += 1
    run = all_pass + all_fail + all_block
    print("*******caseNum : %d, all run : %d, not run : %d*******" % (casenum,run,all_no_run))
    return casenum,run,all_no_run

if __name__ == '__main__':
    tps = tlc.getProjectTestPlans("3173")
    runALL = 0
    caseALL = 0
    for tp in tps:
        if len(sys.argv) < 2:
            if tp["name"] == 'Web_Live_H264_mv2.5.1_battest':
                print(tp["name"])
                cases = tlc.getTestCasesForTestPlan(tp["id"])
                caseNum1,run1,notrun1=get_testcasenumber(cases)
                caseALL += caseNum1
                runALL += run1
            elif tp["name"] == 'Web_Live_VP8_mv2.5.1_battest':
                print(tp["name"])
                cases = tlc.getTestCasesForTestPlan(tp["id"])
                caseNum2, run2, notrun2 =get_testcasenumber(cases)
                caseALL += caseNum2
                runALL += run2
            elif tp["name"] == 'Web_RTC_H264_mv2.5.1_battest':
                print(tp["name"])
                cases = tlc.getTestCasesForTestPlan(tp["id"])
                caseNum3, run3, notrun3 =get_testcasenumber(cases)
                caseALL += caseNum3
                runALL += run3
            elif tp["name"] == 'Web_RTC_VP8_mv2.5.1_battest':
                print(tp["name"])
                cases = tlc.getTestCasesForTestPlan(tp["id"])
                caseNum4, run4, notrun4 =get_testcasenumber(cases)
                caseALL += caseNum4
                runALL += run4
        else:
            testPlan = sys.argv[1]
            if tp["name"] == testPlan:
                print(tp["name"])
                cases = tlc.getTestCasesForTestPlan(tp["id"])
                caseNum1,run1,notrun1=get_testcasenumber(cases)
                caseALL += caseNum1
                runALL += run1
    print('\033[1;35m  caseAll:%d, run:%d, rate:%0.2f \033[0m'%(caseALL, runALL, runALL / caseALL))

import requests,re,sys
JENKINS_USER = "******"
JENKINS_PWD = "*****"
formData = {'j_username': JENKINS_USER, 'j_password': JENKINS_PWD}
headers = {'User-Agent': 'Mozilla/5.0 (Windows **********irefox/52.0'}
s = requests.Session()
s.post("http://**jenkins***//j_acegi_security_check", data=formData, verify=False,headers=headers)
def check_sdk_build_env(expectCommit,project):
    r = s.get("http://**jenkins***:8090/view/we*****ploy/job/"+project+"/lastSuccessfulBuild/artifact/T*******uction.js",verify=False)
    t = str(r.content)
    rr = re.compile(r'BUILD (.*?) ')
    sdk_build_info = rr.findall(t)[0]
    assert expectCommit[:5] in sdk_build_info

if __name__ == '__main__':
    args = sys.argv
    expectCommit = args[1]
    project = args[2]
    check_sdk_build_env(expectCommit,project)
import os
import argparse
import paramiko

USER_NAME = 'agora'
REMOTE_HOST = '10.80.1.215'
SSH_PORT = 25553
PWD = 'bestvoip'

def remote_execute_result(remote_ip, user, passwd, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remote_ip, SSH_PORT, user, passwd)
    print "{0} run command :".format(remote_ip), cmd
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read().strip()
    print "Result:", result
    ssh.close()
    return result

def run_tc_remote(ip_list = None, ulbw = None, ullr = None, dlbw = None, dllr = None, clear = None):
    if ip_list == None:
        return False
        
    if clear=="1":
        cmd = '/home/agora/anaconda2/bin/python /home/agora/remote_tc_ctrl/setNetworkByIpEx.py --clear'
    else:
        #cmd = '/home/agora/anaconda2/bin/python /home/agora/remote_tc_ctrl/setNetworkByIpEx.py --iplist %s --ulbw %s --ullr %s --dlbw %s --dllr %s' % (ip_list, ulbw, ullr, dlbw, dllr)
        cmd = '/home/agora/anaconda2/bin/python /home/agora/media_quality_test/network/tools/set_network_by_ip.py --ip_local %s --ulbw %s --ullr %s --dlbw %s --dllr %s' % (ip_list, ulbw, ullr, dlbw, dllr)
    
    return remote_execute_result(REMOTE_HOST, USER_NAME, PWD, cmd)

if __name__ == '__main__':
    #run_tc_remote('192.168.3.111', 1000, 0, 0, 0)
     run_tc_remote('192.168.2.126', 0, 0, 0, 0)

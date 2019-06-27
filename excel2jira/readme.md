## excel2jira

> 方便在Excel上写用例，用例评审后导入jira

* excution
```
1. 下载excel模板编写用例
    - 根据模板编写用例

2. 将用例Excel放至脚本同级目录，暂时只能一次处理一个Excel文件

3. python3 excel2jira.py(或者双击可执行文件)
    - 提示输入jira用户名
    - 提示输入密码
    - 是否需要检查准备导入的case在jira中已存在（选N吧，选Y的话需要等待检查，时间耗时不确定，依据jira case总数来）
```
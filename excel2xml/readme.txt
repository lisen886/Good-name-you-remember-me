使用说明
  1. 将需要转换的excel文件(例如excel2xmlDemo.xlsx) 复制到程序相同文件夹
  2. chmod +x excel2xml 赋权限(Windows不需要赋权限,直接双击exe文件即可)
  3. 双击excel2xml即可生成xml文件
  4. testLink

Excel模板
  1. 第一行是用例需求名，也将是testLink的文件名
  2. 第一列是测试模块，如果不填就不会新建文件夹
  3. 步骤和预期结果(是以换行"/n"作为步骤分割,自动换行不分割)
       a. 如果步骤和预期结果个数一一对应，testLink也将一一对应
       b. 如果步骤和预期结果个数不对齐，testLink将会将预期结果放置最后一步
# -*- coding: utf-8 -*-
# python3
import xlrd,os,sys
from lxml import etree as lxmlET
# windows打包时需要解决默认编码是ascii
# reload(sys)
# sys.setdefaultencoding('utf-8')

def generate_xml(file):
    workbook = xlrd.open_workbook(file)
    sheet = workbook.sheet_by_index(0)
    folder = sheet.row_values(0)[0]
    importanceDict = {
        "低":"1",
        "中":"2",
        "高":"3"
    }
    '''
    合并单元格的值存储在字典中
    '''
    merged_cell_dict ={}
    for merged_cell in sheet.merged_cells:
        if merged_cell[1] == merged_cell[0]+1:
            merged_cell_value = sheet.cell_value(merged_cell[0], merged_cell[2])
            for j in range(merged_cell[2],merged_cell[3]):
                merged_cell_dict[merged_cell[0],j] = merged_cell_value
        elif merged_cell[3] == merged_cell[2]+1:
            merged_cell_value = sheet.cell_value(merged_cell[0], merged_cell[2])
            for k in range(merged_cell[0], merged_cell[1]):
                merged_cell_dict[k,merged_cell[2]] = merged_cell_value

    tc_root = lxmlET.Element('testsuite', {'name': ''})
    lxmlET.SubElement(tc_root, 'node_order').text = lxmlET.CDATA('')
    lxmlET.SubElement(tc_root, 'details').text = lxmlET.CDATA('')
    xml_file_name = file[:-4] + 'xml'
    folder_node = lxmlET.SubElement(tc_root, 'testsuite', {'name': folder})
    lxmlET.SubElement(folder_node, 'node_order').text = lxmlET.CDATA('')
    lxmlET.SubElement(folder_node, 'details').text = lxmlET.CDATA('')
    for i in range(2,sheet.nrows):
        if sheet.cell_value(i,0) != "":
            childrenFolder_node = lxmlET.SubElement(folder_node, 'testsuite', {'name': sheet.cell_value(i,0)})
            lxmlET.SubElement(childrenFolder_node, 'node_order').text = lxmlET.CDATA('')
            lxmlET.SubElement(childrenFolder_node, 'details').text = lxmlET.CDATA('')
        elif sheet.cell_value(i,0) == "" and (i,0) not in merged_cell_dict.keys():
            step_ts_node = lxmlET.SubElement(folder_node, 'testcase', {'name': sheet.cell_value(i, 1)})
            lxmlET.SubElement(step_ts_node, 'node_order').text = lxmlET.CDATA('')
            lxmlET.SubElement(step_ts_node, 'externalid').text = lxmlET.CDATA('')
            lxmlET.SubElement(step_ts_node, 'version').text = lxmlET.CDATA('1')
            lxmlET.SubElement(step_ts_node, 'summary').text = lxmlET.CDATA('')
            lxmlET.SubElement(step_ts_node, 'preconditions').text = lxmlET.CDATA(sheet.cell_value(i, 2))
            lxmlET.SubElement(step_ts_node, 'execution_type').text = lxmlET.CDATA('1')
            lxmlET.SubElement(step_ts_node, 'importance').text = lxmlET.CDATA(importanceDict[str(sheet.cell_value(i, 5))])
            lxmlET.SubElement(step_ts_node, 'status').text = lxmlET.CDATA('7')

            steps = lxmlET.SubElement(step_ts_node, 'steps')
            stepList = sheet.cell_value(i, 3).split("\n")
            expectRequestList = sheet.cell_value(i, 4).split("\n")
            for stepi in range(0, len(stepList)):
                step = lxmlET.SubElement(steps, 'step')
                lxmlET.SubElement(step, 'step_number').text = lxmlET.CDATA(str(stepi+1))
                lxmlET.SubElement(step, 'actions').text = lxmlET.CDATA(stepList[stepi])
                lxmlET.SubElement(step, 'expectedresults').text = lxmlET.CDATA(expectRequestList[stepi])
                lxmlET.SubElement(step, 'execution_type').text = lxmlET.CDATA('1')

            kws = lxmlET.SubElement(step_ts_node, 'keywords')
            kwList = sheet.cell_value(i, 6).split("\n")
            for kwi in range(0, len(kwList)):
                kw = lxmlET.SubElement(kws, 'keyword', {'name': kwList[kwi]})
                lxmlET.SubElement(kw, 'notes').text = lxmlET.CDATA(kwList[kwi])
            continue

        step_ts_node = lxmlET.SubElement(childrenFolder_node, 'testcase', {'name': sheet.cell_value(i, 1)})
        lxmlET.SubElement(step_ts_node, 'node_order').text = lxmlET.CDATA('')
        lxmlET.SubElement(step_ts_node, 'externalid').text = lxmlET.CDATA('')
        lxmlET.SubElement(step_ts_node, 'version').text = lxmlET.CDATA('1')
        lxmlET.SubElement(step_ts_node, 'summary').text = lxmlET.CDATA('')
        lxmlET.SubElement(step_ts_node, 'preconditions').text = lxmlET.CDATA(sheet.cell_value(i, 2))
        lxmlET.SubElement(step_ts_node, 'execution_type').text = lxmlET.CDATA('1')
        lxmlET.SubElement(step_ts_node, 'importance').text = lxmlET.CDATA(importanceDict[str(sheet.cell_value(i, 5))])
        lxmlET.SubElement(step_ts_node, 'status').text = lxmlET.CDATA('7')
        steps = lxmlET.SubElement(step_ts_node, 'steps')
        stepList = sheet.cell_value(i, 3).split("\n")
        expectRequestList = sheet.cell_value(i, 4).split("\n")
        for stepi in range(0, len(stepList)):
            step = lxmlET.SubElement(steps, 'step')
            lxmlET.SubElement(step, 'step_number').text = lxmlET.CDATA(str(stepi + 1))
            lxmlET.SubElement(step, 'actions').text = lxmlET.CDATA(stepList[stepi])
            lxmlET.SubElement(step, 'expectedresults').text = lxmlET.CDATA(expectRequestList[stepi])
            lxmlET.SubElement(step, 'execution_type').text = lxmlET.CDATA('1')
        kws = lxmlET.SubElement(step_ts_node, 'keywords')
        kwList = sheet.cell_value(i, 6).split("\n")
        for kwi in range(0, len(kwList)):
            kw = lxmlET.SubElement(kws, 'keyword', {'name': kwList[kwi]})
            lxmlET.SubElement(kw, 'notes').text = lxmlET.CDATA(kwList[kwi])
    f = open(xml_file_name, 'wb')
    f.write(lxmlET.tostring(tc_root, xml_declaration=True, encoding='utf-8', pretty_print=True))
    f.close()

def get_excelfile(path):
    L = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.xlsx':
                L.append(path + '/' + file)
        if len(L) == 0:
            print(path + '\nThere is no Excel file,Please check out!')
        return L

if __name__ == '__main__':
#    path = os.getcwd()  # for windows or pycharm
    path = os.path.dirname(sys.executable)  # for mac
    file = get_excelfile(path)
    generate_xml(file[0])

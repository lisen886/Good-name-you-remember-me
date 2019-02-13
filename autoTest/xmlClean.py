#coding=utf-8

import xml.dom.minidom as xmldom

domobj = xmldom.parse("/Users/lisen/Desktop/test.xml")
elementobj = domobj.documentElement
subElementObj = elementobj.getElementsByTagName("test-case")
print(len(subElementObj))
for elem in subElementObj:
    print(elem.getAttribute("status"))
    print(elem.getElementsByTagName("name")[0].firstChild.data)

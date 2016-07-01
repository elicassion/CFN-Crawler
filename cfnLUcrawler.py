# -*- coding:utf8 -*-
import codecs
import json
import re
import os
import urllib
import urllib2
import urlparse
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from collections import defaultdict
from bs4 import BeautifulSoup

url = "http://sccfn.sxu.edu.cn/portal-zh/lexical-unit.aspx"
folder = "cfn_lu"
filename = "lunit.json"
lunitDicArray = []
lunitBigDic = {}

if not os.path.exists(folder):
	os.mkdir(folder)
res = urllib2.urlopen(url, timeout = 3)
content = res.read()
parsedContent = BeautifulSoup(content, "html.parser")
luInfo = parsedContent.find("ul", id = "list_lunit")
#print luInfo
for lunit in luInfo:
	if not isinstance(lunit, type(luInfo)):
		continue
	wAPos = lunit.find("span", class_ = "lunit").string
	word = wAPos.split("/")[0][:-1]
	word.replace("“","")
	word.replace("”", "")
	pos = wAPos.split("/")[1]
	#print "word: ", word
	#print "pos: ", pos
	a = lunit.find("a")
	href = a.get("href")
	frameId = href.split("=")[1]
	#print "frameId: ", frameId
	frameName = a.string[1:-1]
	#print "framName: ", frameName
	#print "---------------------"
	lunitDic = lunitBigDic.get(word, {})
	if not lunitDic.has_key("frames"):
		lunitDic["frames"] = []
	framesList = lunitDic.get("frames", [])
	sgFrameDic = {}
	sgFrameDic["pos"] = pos
	sgFrameDic["frameId"] = int(frameId)
	sgFrameDic["frameName"] = frameName
	lunitDic["frames"].append(sgFrameDic)
	lunitDic["word"] = word
	lunitBigDic[word] = lunitDic

for (k, v) in lunitBigDic.items():
	lunitDicArray.append(v)

lunitFile = codecs.open(os.path.join(folder, filename), "w")
lunitFile.write(json.dumps(lunitDicArray, ensure_ascii = False, indent = 4))
lunitFile.close()

print "---------FINISHED---------"
print "LUNumber: ", str(len(lunitDicArray))


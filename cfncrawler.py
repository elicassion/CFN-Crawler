# -*- coding:utf8 -*-
# max = 512
# except in nonexistence.txt

import codecs
import json
import re
import os
import urllib
import urllib2
import urlparse
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from bs4 import BeautifulSoup

urlRoot = "http://sccfn.sxu.edu.cn/portal-zh/frame-details.aspx?id="
folder = "cfn_frame"
nonExistenceFilename = "nonexistence.txt"
validFrameNumber = 0
frameElmtNumber = 0
coreFrameElmtNumber = 0
nonCoreFrameElmtNumber = 0
lexElmtNumber = 0




def getPage(url):
	try:
		res = urllib2.urlopen(url, timeout = 3)
		content = res.read()
	except:
		return ''
	else:
		return content

def analyzeFdInfo(fdInfo):
	fdInfoDic = {}
	keys = ["cName", "eName", "des"]
	keyNumber = 0
	for tr in fdInfo:
		if not isinstance(tr, type(fdInfo)):
			continue
		fdInfoDic[keys[keyNumber]] = tr.td.string
		keyNumber += 1
	return fdInfoDic

def analyzeFeInfo(feInfo):
	global frameElmtNumber, coreFrameElmtNumber, nonCoreFrameElmtNumber
	#print feInfo
	
	keys = ["#", "cName", "eName", "abbrName", "isCore", "def"]
	elmtDicArray = []
	isFirst = False
	for tr in feInfo:
		#print tr
		if not isinstance(tr, type(feInfo)):
			continue
		if not isFirst:
			isFirst = True
			continue
		elmtDic = {}
		keyNumber = -1;
		for td in tr:
			if not isinstance(td, type(feInfo)):
				continue
			keyNumber += 1
			if (keyNumber <= 0):
				continue
			if (keyNumber == 4):
				if (td.string == "True"):
					elmtDic[keys[keyNumber]] = True
					coreFrameElmtNumber += 1
				else:
					elmtDic[keys[keyNumber]] = False
					nonCoreFrameElmtNumber += 1
			else:
				elmtDic[keys[keyNumber]] = td.string
			#print td.string
		frameElmtNumber += 1
		elmtDicArray.append(elmtDic)
	return elmtDicArray

def analyzeLexElmt(lexElmtInfo):
	global lexElmtNumber
	lexElmtDicArray = []
	lexElmtInfo = "".join(lexElmtInfo.split())
	for elmt in lexElmtInfo.split(";"):
		if elmt == "":
			continue
		lexElmtDic = {}
		array = elmt.split("/")
		lexElmtDic["word"] = array[0]
		lexElmtDic["POS"] = array[1]
		lexElmtNumber += 1
		lexElmtDicArray.append(lexElmtDic)
	return lexElmtDicArray

def analyzeContent(content, frameNumber):
	frameDic = {}

	parsedContent = BeautifulSoup(content, "html.parser")
	fdInfo =  parsedContent.find("table", id = "fd_box")
	frameDic["fdInfo"] = analyzeFdInfo(fdInfo)
	
	feInfo = parsedContent.find("table", id = "fe_box")
	frameDic["element"] = analyzeFeInfo(feInfo)

	lexElmtInfo = parsedContent.form.contents[14]
	frameDic["lexElmt"] = analyzeLexElmt(lexElmtInfo)

	file = codecs.open(os.path.join(folder, str(frameNumber)+".json"), "w")
	file.write(json.dumps(frameDic, ensure_ascii = False, indent = 4))
	file.close()


def dealPage(url, frameNumber):
	content = getPage(url)
	if "查询结果为空" in content:
		return False
	else:
		analyzeContent(content, frameNumber)
		return True

for frameNumber in range(1, 513):
	if not os.path.exists(folder):
		os.mkdir(folder)
	print "cur: " + str(frameNumber)
	url = urlRoot + str(frameNumber)
	if not dealPage(url, frameNumber):
		print str(frameNumber) + " does not exist."
		nexfile = codecs.open(os.path.join(folder, nonExistenceFilename), "a")
		nexfile.write(str(frameNumber)+"\n")
		nexfile.close()
	else:
		validFrameNumber += 1
print "-------------FINISHED-------------"
print "Valid Frame Number: ", validFrameNumber
print "Frame Element Number: ", frameElmtNumber
print "Core Frame Element Number: ", coreFrameElmtNumber
print "Non-Core Frame Element Number: ", nonCoreFrameElmtNumber
print "Lexical Element Number: ", lexElmtNumber
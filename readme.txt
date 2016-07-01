爬取框架信息存储为json格式，文件名命名为 框架编号.json 编码格式utf8
json结构:
	fdInfo(Object):<储存框架的基本信息>
		cName(String):<中文名>
		eName(String):<英文名>
		des(String):<描述>
	element(Array):<框架元素>
		单个Object{
			cName(String):<中文名>
			eName(String):<英文名>
			abbrName(String):<缩写>
			isCore(Bool):<是否是核心框架元素>
			def(String):<定义>
		}
	lexElmt(Array):<词元>
		单个Object{
			word(String):<词>
            POS(String):<词性> (a,b,c,d,e,f,i,n,p,q,r,u,v,nz)
		}

不存在的框架编号存储在nonexistence.txt中 每行一个

stadata.txt存储统计信息，每行一项，包括：
	总框架数
	总框架元素数
	总核心框架元素数
	总非核心框架元素数
	总词元数
	词性类别数
	词性类别(按频度降序排列，格式: pos:数量，用逗号“,”隔开)

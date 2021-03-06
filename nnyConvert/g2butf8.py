#-*- coding: utf8 -*-

import sys
import os
import codecs
import shutil
from glob import glob
import ConfigParser
from jianfan import jtof
# http://code.google.com/p/python-jianfan/
#import chardet
from chardet.universaldetector import UniversalDetector
# http://chardet.feedparser.org
from dic_tw import dic_tw

# 最大正向匹配
def convertVocabulary(string_in, dic):
    i = 0
    while i < len(string_in):
        for j in range(len(string_in) - i, 0, -1):
            if string_in[i:][:j] in dic:
                t = dic[string_in[i:][:j]]
                string_in = string_in[:i] + t + string_in[i:][j:]
                i += len(t) - 1
                break
        i += 1
    return string_in
	
def getEncoding(filename):
	fp = open(filename, 'r')
	orig_content = fp.read()
	detector = UniversalDetector()
	detector.feed(orig_content)
	detector.close()
	fp.close()
	return detector.result["encoding"]

	
	
def getEncodingByContent(content):
	detector = UniversalDetector()
	detector.feed(content)
	detector.close()
	return detector.result["encoding"]

# get user define dictionary
def getUserDic(filename):
	user_dic= {}
	if os.path.exists(filename):
		f_encoding = getEncoding(filename)
		if f_encoding == None:
			print (u"抱歉, 未能正確判斷自定字典編碼！\n\n");
		else:
			fpr = open(filename, 'r');
			lines = fpr.readlines();
			fpr.close();

			if lines[0].startswith(codecs.BOM_UTF8 ):
				lines[0] = lines[0].lstrip(codecs.BOM_UTF8 );
				
			for line  in lines:
				line = line.decode(f_encoding);
				words = line.split('=')
				key = words[0].lstrip().rstrip();
				value = words[1].lstrip().rstrip();
				user_dic[key] = value;

		return user_dic
	
#user dictionary file
user_dic_file = 'userdic.txt'
	
# start error message

MSG_USAGE = u"使用方法： g2butf8 [filename] 會自動偵測編碼，再轉換成有BOM的UTF-8"
MSG_TEXT_FILE_NOT_FOUND = u"錯誤 - 檔案找不到："
MSG_CONVERT_FINISH = u"轉換成功！\n"
MSG_NO_CONVERT = u"檔案長度為零，不做轉換\n"
# end of error message

# start parse parameters

argc = len(sys.argv)

if argc > 3 or argc == 1:
    sys.exit (MSG_USAGE);

# end of parse parameters.

dir_separator = os.path.sep


def convertFile(target_file):
	user_dic= {}
	if os.path.exists(target_file):
		f_encoding = getEncoding(target_file)
		print u"正在轉換", target_file, u" 編碼為: ", f_encoding
		if f_encoding == None:
			print (u"抱歉, 未能正確判斷編碼！\n\n");
		else:
			result_content = u''
			original_content = u''
			fp = open(target_file, 'r')
			original_content = fp.read()
			fp.close()
			
			if original_content.startswith( codecs.BOM_UTF8 ):
				original_content = original_content.lstrip( codecs.BOM_UTF8);	
			
			utf8content=original_content.decode(f_encoding)

			newcontent = jtof(utf8content)
			lines = newcontent.splitlines();
			for line in lines:
				line = convertVocabulary(line, dic_tw());
				
			if os.path.getsize(target_file) > 0:
				# do backup
				backup_file = target_file + '.bak'
				shutil.copy2(target_file, backup_file)
				fpw = open(target_file, 'w')
				if not newcontent.startswith(codecs.BOM_UTF8.decode( "utf8" )):
					fpw.write(codecs.BOM_UTF8)

				pathdir =os.path.dirname(os.path.abspath(target_file));
				user_dic_pathname = pathdir +os.path.sep+user_dic_file;
				
				if os.path.exists(user_dic_pathname):
					user_dic = getUserDic(user_dic_pathname);
					if len(user_dic) > 0:
						for line in lines:
							line = convertVocabulary(line,  user_dic);

				for line in lines:
					line = convertVocabulary(line,  user_dic);
					fpw.write(line.encode('UTF-8'))
					fpw.write("\n");
				fpw.close();
				
				print (MSG_CONVERT_FINISH)
			else:
				print MSG_NO_CONVERT
			
			
if __name__ == "__main__":
	#主程序
	filelist = glob(sys.argv[1])
	for afile in filelist:
		convertFile(afile);


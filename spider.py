import requests
import re
import pymysql

db = pymysql.connect(host="localhost", user="root", password="pw", database="webinfo",charset='utf8')
cursor = db.cursor()

headers = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66',}

url1 = 'http://cs.hitsz.edu.cn/szll/qzjs.htm'

data = requests.get(url1,headers=headers)
data.encoding = 'utf-8'
baseInfo = data.text

teacherInfo = re.findall(r'<div class="teacher-left">',baseInfo) # 页面里面有多少个<div class="teacher-left">，这说明页面里有多少教师信息

teacherName = re.findall(r'<p class="teacher-name">(.*?)</p>',baseInfo)
teacherTitle = re.findall(r'<dt>任职：</dt><dd>(.*?)</dd>',baseInfo)
teacherTelephone = re.findall(r'<dt>电话：</dt><dd> (.*?)</dd>',baseInfo) # 这个地方网页上有一个空格，注意
teacherFax = re.findall(r'<dt>传真：</dt><dd> (.*?)</dd>',baseInfo) # 这个地方网页上有一个空格，注意
teacherEmail = re.findall(r'<dt>Email：</dt><dd><a href="mailto:(.*?)">',baseInfo)
teacherField = re.findall(r'<dt>研究方向：</dt><dd>(.*?)</dd>',baseInfo)

for i in range(1,6):
    url2 = 'http://cs.hitsz.edu.cn/szll/qzjs/{}.htm'.format(i)
    data1 = requests.get(url2, headers=headers)
    data1.encoding = 'utf8'
    baseInfo1 = data1.text
    teacherInfo1 = re.findall(r'<div class="teacher-left">',baseInfo1)
    teacherName1 = re.findall(r'<p class="teacher-name">(.*?)</p>', baseInfo1)
    teacherTitle1 = re.findall(r'<dt>任职：</dt><dd>(.*?)</dd>', baseInfo1)
    teacherTelephone1 = re.findall(r'<dt>电话：</dt><dd> (.*?)</dd>', baseInfo1)
    teacherFax1 = re.findall(r'<dt>传真：</dt><dd> (.*?)</dd>', baseInfo1)
    teacherEmail1 = re.findall(r'<dt>Email：</dt><dd><a href="mailto:(.*?)">', baseInfo1)
    teacherField1 = re.findall(r'<dt>研究方向：</dt><dd>(.*?)</dd>', baseInfo1)

    teacherInfo.extend(teacherInfo1)
    teacherName.extend(teacherName1)
    teacherTitle.extend(teacherTitle1)
    teacherTelephone.extend(teacherTelephone1)
    teacherFax.extend(teacherFax1)
    teacherEmail.extend(teacherEmail1)
    teacherField.extend(teacherField1)

for j in range(0,len(teacherInfo)):
    sql = 'insert into `teacher`(`name`,`title`,`telephone`,`fax`,`email`,`field`) values ("{}","{}","{}","{}","{}","{}")'.format(teacherName[j],teacherTitle[j],teacherTelephone[j],teacherFax[j],teacherEmail[j],teacherField[j])
    cursor.execute(sql)
    db.commit()
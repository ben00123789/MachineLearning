# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 12:48:49 2018

@author: Ben
"""
"""系統系教師姓名與信箱"""

import requests# 引用 requests 套件

url_1 ='http://w3.sname.ncku.edu.tw/main.php?mod=teacher&'#系統系師資網址
res_1 = requests.get(url_1)# 使用 GET 方式取得網頁
res_1.encoding ='gbf2312'# 將網頁重新編碼

from bs4 import BeautifulSoup as bs# 引用 Beautiful Soup 套件並縮寫為 bs

soup = bs(res_1.text,'html.parser')# 以 Beautiful Soup 解析 HTML 程式碼

import pandas as pd# 引用套件並縮寫為 pd

names = pd.Series()# 宣告 names 為一維的欄位

for i in soup.select("img[src='./modules/teacher/tmpl/images/people.gif']"):# 尋找包含 src 的 tag img 區塊
    names = names.append(pd.Series(i['alt'])).reset_index(drop=True)# 將位於 alt 後的姓名加入 names

import re# 引用套件 re

mails = pd.Series()# 宣告 mails 為一維的欄位
for mail in soup.find_all(href=re.compile("@")):# 尋找包含 @ 的 href
    mails = mails.append(pd.Series([mail.string])).reset_index(drop=True)# 將找到的資料中的字串部分加入 mails
    
df_1 = pd.DataFrame({'姓名':names,'信箱':mails})# 使用 dataframe 將姓名與信箱畫成表格
print(df_1[['姓名','信箱']])# 印出表格

"""門牌程式"""

x = input('請輸入路名：\n')#請求輸入待查詢的路名
payload ={# POST 需要的 data
"ttrstyle":  "2",
"yy": "107",
"mm": "01",
"dd": "16",
"s_yy": "", 
"s_mm": "", 
"s_dd": "", 
"e_yy": "", 
"e_mm": "", 
"e_dd": "", 
"ttrarea": "", 
"ttrstreet": x,
"ttrsection": "", 
"ttrshi": "", 
"ttrlo": "", 
"ttrtemp":"", 
"ttrnum":"", 
"ttrfloor":"", 
"ttrg":"", 
"ttryear":"", 
"ttrmonth":"", 
"ttrday":"", 
"ettryear":"", 
"ettrmonth":"", 
"ettrday":"", 
        }

url_2 = 'http://www.houseno.tcg.gov.tw/ASP_FRONT_END/main_.asp'# 門牌檢索網址
res_2 = requests.post(url_2,data=payload)# 使用 POST 方式取得網頁，並給予需要的 data

soup = bs(res_2.text,'html.parser')# 以 Beautiful Soup 解析 HTML 程式碼

add = []# 宣告 add 為 list
for j in soup.find_all('a'):# 找到網頁中 tag a 包含的區塊
    r = re.sub('[^０-９\u4e00-\u9fff]+', '', j.attrs['href'])# 整理取得的資料，只保留全形數字與中文字
    if r != "":# 若處理完的資料不為空白則存入add
        add.append(r)

df_2 = pd.DataFrame(add, columns = ["address"])# 使用 dataframe 將 add 畫成表格
print(df_2)# 印出表格
    
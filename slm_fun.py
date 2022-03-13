
#%% 1.导入常用包

import pandas as pd
import numpy as np
# from pytz import timezone
# import pytz
from datetime import datetime, timedelta, timezone
from tda import auth, client
import requests
import socket

import time
import json
import os
import sys

# print(1)
# Log(1)

#%% 2.取现在时间（美东时间）

def slm_now_us():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    # us_dt = utc_dt.astimezone(timezone(timedelta(hours=-4)))
    import pytz
    us_dt = utc_dt.astimezone(pytz.timezone('US/Eastern'))
    now1 = us_dt.strftime('%Y-%m-%d %H:%M:%S')
    return(now1)

#%% 3.datetime转为时间戳

# https://tool.chinaz.com/tools/unixtime.aspx

def slm_str2ts(str, tz_hours = -4):
    dt = datetime.strptime(str, "%Y-%m-%d %H:%M:%S")
    tz_utc_4 = timezone(timedelta(hours=tz_hours))
    dt = dt.replace(tzinfo=tz_utc_4)
    ts = dt.timestamp()
    return(ts)

#%% 4.时间戳转为str

def slm_ts2str(ts, tz_hours = -4):
    tz_utc_4 = timezone(timedelta(hours=tz_hours))
    import pandas as pd
    datetime1 = pd.to_datetime(ts, unit='s', utc=True).tz_convert(tz_utc_4)
    str1 = str(datetime1)[:19]
    return(str1)

#%% 5.循环导入csv直至成功

def slm_fmz_read_csv(add, index_col=0):
    is_error=1
    while is_error==1:
        try:
            df=pd.read_csv(add, index_col=index_col)
        except:
            Log(add, '导入失败，1s后再试。')
            Sleep(1000)
        else:
            is_error=0
    return(df)

#%% 6.下载我的git文件

def slm_download_git(file_name, out_path):
    zip_url='https://codeload.github.com/zxcvbnm3260/ChristopherShen/zip/refs/heads/master'
    folder_name='ChristopherShen-master'
    zip_inner_path='ChristopherShen-master/'+file_name
    import os
    if os.path.exists('git.zip'): os.remove('git.zip')
    if os.path.exists(out_path): os.remove(out_path)
    import shutil
    if os.path.exists(folder_name): shutil.rmtree(folder_name)
    # Log('完成：删除上次下载的函数库。')

    import wget
    wget.download(zip_url, 'git.zip')
    # Log('完成：下载zip。')

    import zipfile
    zip_file = zipfile.ZipFile('git.zip')
    zip_file.extract(zip_inner_path)
    # Log('完成：解压缩。')

    shutil.copyfile(zip_inner_path, out_path)
    # Log('完成：复制到指定目录下。')

#%% 7.从csv导入stock_list

def slm_stock_list_from_csv(con='a1.exclude==0'):
    wd1 = os.getcwd()
    add1 = wd1 + '/fmz/price_stock/stock_list.csv'
    # 从我的git上下载stock_list：
    slm_download_git(file_name='stock_list.csv', out_path=add1)
    while not os.path.exists(add1):
        Log('stock_list为空，等待创建，2秒后再看……')
        Sleep(2000)

    a1 = slm_fmz_read_csv(add1,index_col=0)
    a1 = a1[eval(con)]
    a2 = a1.loc[eval(con),'code'].to_list()
    a3 = list(set(a2))
    if len(a2)!=len(a3):
        Log('stock_list有重复！')
        exit()
    stock_list=a2
    return([stock_list, a1])

def slm_futures_list_from_csv(con='a1.exclude==0'):
    wd1 = os.getcwd()
    add1 = wd1 + '/fmz/price_stock/futures_list.csv'
    # 从我的git上下载stock_list：
    slm_download_git(file_name='futures_list.csv', out_path=add1)
    while not os.path.exists(add1):
        Log('futures_list为空，等待创建，2秒后再看……')
        Sleep(2000)

    a1 = slm_fmz_read_csv(add1, index_col=0)
    # a1 = a1[eval(con)]
    # a2 = a1.loc[eval(con),'code'].to_list()
    a2 = a1.loc[:,'code'].to_list()
    a3 = list(set(a2))
    if len(a2)!=len(a3):
        Log('stock_list有重复！')
        exit()
    stock_list=a2
    return([stock_list, a1])

#%% 8.从git下载字体文件

def slm_plt_font(font_file='simhei.ttf'):
    wd1=os.getcwd()
    add1=wd1+'/fmz/font/'
    if not os.path.exists(add1): os.makedirs(add1)
    add2=add1+font_file
    # 从我的git上下载stock_list：
    slm_download_git(file_name=font_file, out_path=add2)
    from matplotlib.font_manager import FontProperties
    font = FontProperties(fname=add2)
    return(font)

# %% 9.前n个交易日是哪天？（含输入日）

def slm_previous_tradedays(date, n): 
    import os 
    # 读取交易日表
    ADD01 = os.getcwd() + '/fmz/price_stock/tradeday_list.csv'
    if not os.path.exists(ADD01): slm_download_git(file_name = 'tradeday_list.csv', out_path = ADD01)
    TRADEDAY_DF = slm_fmz_read_csv(ADD01, index_col=0)

    i = TRADEDAY_DF.index.values[TRADEDAY_DF.date==date][0]
    j = -1
    while True:
        is_tradeday = TRADEDAY_DF.loc[i, 'is_tradeday']
        date1 = TRADEDAY_DF.loc[i, 'date']
        if is_tradeday==1: 
            j += 1
            if j==n: return date1
        i -= 1

# %% 10.两日期相差多少个交易日
def slm_how_many_tradedays(date1, date2):
    import os 
    # 读取交易日表
    ADD01 = os.getcwd() + '/fmz/price_stock/tradeday_list.csv'
    if not os.path.exists(ADD01): slm_download_git(file_name = 'tradeday_list.csv', out_path = ADD01)
    TRADEDAY_DF = slm_fmz_read_csv(ADD01, index_col=0)
    index1 = TRADEDAY_DF.index.values[TRADEDAY_DF.date==date1][0]
    index2 = TRADEDAY_DF.index.values[TRADEDAY_DF.date==date2][0]
    return sum(TRADEDAY_DF.loc[index1:index2, 'is_tradeday'])

#%% FMZ相关函数

#%%% 1.FMZ函数本地化

# 识别是否FMZ运行
# is_fmz= 1 if sys.platform=='linux' else 0

# COMPUTERNAME=os.getenv('COMPUTERNAME', 'defaultValue')
# if COMPUTERNAME=='SLM-VULTR-WIN': is_fmz=1

# 必须在脚本正文中才有效：
# try:
#     IsVirtual()
# except NameError:
#     is_fmz=0
# else:
#     is_fmz=1

# Log('是否在FMZ上运行？is_fmz=', is_fmz)
# if is_fmz==0:
#     Log=print
#     LogStatus=print

# def Sleep(n):
#     global is_fmz
#     if is_fmz==0: time.sleep(n/1000)


# 无效：
# def _D():
#     if is_fmz==0: slm_now_us()

#%%% 2.df转为FMZ的table

def slm_fmz_df2table(df):
    columns = df.columns.values.tolist()

    import copy
    df2 = copy.deepcopy(df)
    for c in range(df.shape[1]):
        df2.iloc[:, c] = df.iloc[:, c].astype(str)

    for i in range(df2.shape[0]):
        row_i = df2[i:(i+1)].values.tolist()
        if i==0: 
            rows = copy.deepcopy(row_i)
        else: rows = rows + row_i
    return([columns, rows])


# %% 草稿


#%% 1.导入常用包

import pandas as pd
import numpy as np
# from pytz import timezone
# import pytz
from datetime import datetime, timedelta, timezone
from tda import auth, client
import requests

import time
import json
import os
import sys
# print(1)

#%% 2.df转为FMZ的table

def slm_df2table(df):
    columns = df.columns.values.tolist()
    for i in range(df.shape[0]):
        row_i=df[i:(i+1)].values.tolist()
        if i==0: rows=row_i
        else: rows=rows+row_i
    return([columns,rows])

#%% 3.datetime转为时间戳

# https://tool.chinaz.com/tools/unixtime.aspx

def slm_str2ts(str, tz_hours=-4):
    dt = datetime.strptime(str, "%Y-%m-%d %H:%M:%S")
    tz_utc_4 = timezone(timedelta(hours=tz_hours))
    dt = dt.replace(tzinfo=tz_utc_4)
    ts=dt.timestamp()
    return(ts)

#%% 4.时间戳转为str

def slm_ts2str(ts, tz_hours=-4):
    tz_utc_4 = timezone(timedelta(hours=tz_hours))
    import pandas as pd
    datetime1 = pd.to_datetime(ts, unit='s', utc=True).tz_convert(tz_utc_4)
    str1 = str(datetime1)[:19]
    return(str1)

#%% 5.取现在时间（美东时间）

def slm_now_us():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    us_dt = utc_dt.astimezone(timezone(timedelta(hours=-4)))
    now1 = us_dt.strftime('%Y-%m-%d %H:%M:%S')
    return(now1)

#%% 6.循环导入csv直至成功

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

#%% 7.FMZ函数本地化

# 识别是否FMZ运行
# try:
#     IsVirtual()
# except NameError:
#     is_fmz=0
# else:
#     is_fmz=1

is_fmz= 1 if sys.platform=='linux' else 0

COMPUTERNAME=os.getenv('COMPUTERNAME', 'defaultValue')
if COMPUTERNAME=='SLM-VULTR-WIN': is_fmz=1

if is_fmz==0:
    log=print
    # LogStatus=print
else:
    log=Log
    # LogStatus=LogStatus

log('是否在FMZ上运行：is_fmz=', is_fmz)

def Sleep(n):
    if is_fmz==0: time.sleep(n/1000)

# 无效：
# def _D():
#     if is_fmz==0: slm_now_us()

#%% 8.下载git文件

def slm_download_git(file_name, out_path):
    zip_url='https://codeload.github.com/zxcvbnm3260/ChristopherShen/zip/refs/heads/master'
    folder_name='ChristopherShen-master'
    zip_inner_path='ChristopherShen-master/'+file_name
    import os
    if os.path.exists('git.zip'): os.remove('git.zip')
    if os.path.exists(out_path): os.remove(out_path)
    import shutil
    if os.path.exists(folder_name): shutil.rmtree(folder_name)
    Log('完成：删除上次下载的函数库。')

    import wget
    wget.download(zip_url, 'git.zip')
    Log('完成：下载zip。')

    import zipfile
    zip_file = zipfile.ZipFile('git.zip')
    zip_file.extract(zip_inner_path)
    Log('完成：解压缩。')

    shutil.copyfile(zip_inner_path, out_path)
    Log('完成：复制到指定目录下。')




# %% 草稿

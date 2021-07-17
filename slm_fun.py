
#%% 0.导入常用包

import pandas as pd
import numpy as np
from pytz import timezone
from datetime import datetime, timedelta, timezone
import time
import json
import os
import sys
from tda import auth, client

# print(1)

#%% 1.df转为FMZ的table

def slm_df2table(df):
    columns = df.columns.values.tolist()
    for i in range(df.shape[0]):
        row_i=df[i:(i+1)].values.tolist()
        if i==0: rows=row_i
        else: rows=rows+row_i
    return([columns,rows])

#%% 2.datetime转为时间戳

# https://tool.chinaz.com/tools/unixtime.aspx

def slm_str2ts(str, tz_hours=-4):
    dt = datetime.strptime(str, "%Y-%m-%d %H:%M:%S")
    tz_utc_4 = timezone(timedelta(hours=tz_hours))
    dt = dt.replace(tzinfo=tz_utc_4)
    ts=dt.timestamp()
    return(ts)

#%% 3.时间戳转为str

def slm_ts2str(ts, tz_hours=-4):
    tz_utc_4 = timezone(timedelta(hours=tz_hours))
    import pandas as pd
    datetime1 = pd.to_datetime(ts, unit='s', utc=True).tz_convert(tz_utc_4)
    str1 = str(datetime1)[:19]
    return(str1)

#%% 4.取现在时间（美东时间）

def slm_now_us():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    us_dt = utc_dt.astimezone(timezone(timedelta(hours=-4)))
    now1 = us_dt.strftime('%Y-%m-%d %H:%M:%S')
    return(now1)

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

#%% 6.FMZ的Log本地化

# _D()
# LogStatus

def Sleep(n):
    if sys.platform=='linux':
        Sleep(n)
    else:
        time.sleep(n)

# def Log(str):
#     if sys.platform=='linux':
#         Log(str)
#     else:
#         print(str)

# def Log(*objects):
#     if sys.platform=='linux':
#         Log(*objects)
#     else:
#         print(*objects)


# %% 草稿

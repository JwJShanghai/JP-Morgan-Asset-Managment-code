import numpy as np
import math
import pandas as pd
import xlwt

S_start=pd.read_excel(r"C:\Users\JwJShanghai\Desktop\数据1.xlsx")
s_start=S_start.values
S_inital=[]
for j in range(14):
    S_inital.append(s_start[0][j]) #读取每个资产的初始收益率数据


S_char=pd.read_excel(r"C:\Users\JwJShanghai\Desktop\Monte carlo.xlsx")
s_char=S_char.values
s_mean_var=[]
for j in range(14):
    s_mean_var.append([s_char[0][j]])
    s_mean_var[j].append(s_char[1][j]) #读取每个资产的收益率和方差

f = xlwt.Workbook()
sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True) 

#每个资产走12次
for m in range(0,100):
    S_price=[]
    S=[1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    for j in range(14):
        S[0]= S_inital[j]
        S_price.append([S[0]])
        miu=s_mean_var[j][0]
        sigma=s_mean_var[j][1]  
        for t in range(1,13):
            S[t]=S[t-1]+S[t-1]*miu*1+sigma*S[t-1]*np.random.normal(0,1)*np.sqrt(1) #此处的dt时间间隔假设为1
            S_price[j].append(S[t])
    for j in range(14):
        for t in range(1,13):
            sheet1.write(t+m*12,j,S_price[j][t])
f.save(r'D:\test3.xls') 

#for i in range(100):
    



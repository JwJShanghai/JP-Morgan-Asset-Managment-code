#欢迎来到 Black-Litterman模型代码实现。代码有些许复杂，是因为这是我们整个回测框架的一部分。
import pandas as pd
import numpy as np
from cvxopt import matrix, solvers
import xlwt
import random

K=pd.read_excel(r'C:\Users\JwJShanghai\Desktop\State-Forecast.xlsx')
M=K.values
N=["deflationary","inflationary","reflationary","stagflationary"]
State=[]
for i in range(len(M)):
    State.append(N.index(M[i][0]))

def blacklitterman_weight_result(df,state_number):
    riskaverse=10
    PAI=np.matrix(df.mean()).T
    Epsilon=np.matrix(df.cov())
    P=matrix(np.eye(14))#P是信息矩阵
    P=np.matrix(P)
    
    Q_deflation=[-0.0072,-0.0070,-0.0074,-0.0088,-0.0044,-0.0105,-0.0098,-0.012,0.0065,0.0020,0.0032,0.0065,0.0038,0.0047]
    Q_inflation=[0.0196,0.0192,0.0243,0.0254,0.0248,0.0151,0.0190,0.0222,0.0063,0.0020,0.0032,0.0062,0.0038,0.0047]
    Q_reflation=[0.0129,0.0124,0.0148,0.0163,0.0122,0.0138,0.0084,0.00984,0.0066,0.0019,0.0033,0.0061,0.0038,0.0046]
    Q_stagflation=[0.0169,0.0167,0.0160,0.0182,0.0172,0.0188,0.0121,0.0034,0.0055,0.0020,0.0029,0.0063,0.0034,0.0045] 
    if State[state_number]== 0:
        Q=Q_deflation
    if State[state_number]==1:
        Q=Q_inflation
    if State[state_number]==2:
        Q=Q_reflation
    if State[state_number]==3:
        Q=Q_stagflation

 #Q是相对收益率，或者预期收益率
    Q=np.matrix(matrix(Q)) #绝对观点矩阵Q
    O=np.matrix(0.1*np.eye(len(df.columns))) #绝对观点偏误矩阵omega
    tao=0.05 #不确定性度量tao
    miu_bar=((tao*Epsilon).I+P.T*O.I*P).I*((tao*Epsilon).I*PAI+P.T*O.I*Q)    #计算u
    P=riskaverse*matrix(Epsilon)
    P1=riskaverse*matrix(Epsilon) 
    q=-1.0*matrix(miu_bar)
    q1=-1*matrix(df.mean())
    A=[]
    for i in range(len(df.columns)):
        A.append([1.0])
    A=matrix(A)
    b=matrix([1.0]) #此处是Ax=b要求它的和必须为1
    G=matrix(np.row_stack((-1.0*np.eye(14),1.0*np.eye(14))))
    h=matrix(np.row_stack((np.matrix(0*np.ones(14)).T,np.matrix(0.4*np.ones(14)).T)))#添加的条件为占比不得超过±40%
        
    sol1=solvers.qp(P=P1,q=q1,G=G,h=h,A=A,b=b) #此为均值方差的情况
    sol2=solvers.qp(P=P,q=q,G=G,h=h,A=A,b=b) #此为Black-Litterman模型情况
    result1=list(sol1['x'].T)
    result2=list(sol2["x"].T)
    return result1,result2

f = xlwt.Workbook()
sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True) #均值方差结果
sheet2 = f.add_sheet(u'sheet2',cell_overwrite_ok=True) #均值方差结果

df_change=pd.read_excel(r'C:\Users\JwJShanghai\Desktop\2019Forecast.xlsx')
df=df_change[0:12]
df_change_forecast=pd.read_excel(r'C:\Users\JwJShanghai\Desktop\数据2.xlsx')

for k in range(100): #重复100次
    Q=list(df_change_forecast[0+k*12:12+k*12].values)
    for j in range(12):
        df.loc[j+1]=(list(Q[j]))
    #df为每次的收益
    for q in range(12):
        df_used=df[0+q:12+q]
        result1 = blacklitterman_weight_result(df_used,q)
        for i in range(14):
            sheet1.write(q+k*12,i,result1[0][i])
            sheet2.write(q+k*12,i,result1[1][i])
f.save(r'D:\test1.xls') 




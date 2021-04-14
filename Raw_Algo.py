import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data=pd.read_excel('rawwaw.xlsx')
df1=data[['Date/Time','lead_close']]
df2=data[['Date/Time','zinc_close']]
df=pd.merge(df1,df2,on='Date/Time')
df1=df
df1['day']=df1['Date/Time'].dt.day
def zscore(df,x=30):    
    spread=df['lead_close']-df['zinc_close']
    spread_mavg1=spread.rolling(1).mean()
    spread_mavg=spread.rolling(x).mean()
    spread_std=spread.rolling(x).std()
    z_score=(spread_mavg1-spread_mavg)/spread_std
    df['zscore']=z_score
    df.dropna(inplace=True)
    df.reset_index(inplace=True)
    df['zscore'].fillna(0.0, inplace=True)
    df['zscore'].replace([np.inf, -np.inf], 0.0, inplace=True)
    return df


dfx=zscore(df.copy(),30)
dfx['zscore'].plot(kind='hist',bins=1000)
test=dfx[0:100]
def market_signals(pair,z_entry=1,z_exit=0.1):
    k=0
    pair['position']=0
    long_market = 0
    short_market = 0
    pair['return']=0
    pair['pnl']=0
    trade=0
    buy=0
    sell=0
    y=0
    z=0
    #num1=pair.index[100]
    #num2=pair.index[200]
    pair.reset_index(drop=True)
    for i in range(1,len(pair)-1):
        
        z=0
        row1=pair.iloc[i+1]
        row=pair.iloc[i]
        rowpre=pair.iloc[i-1]
        #pair.loc[i,['return']]=row['total']+rowpre['return']
        if (trade!=0) and (rowpre['zscore']*row['zscore']<0 or abs(row['zscore'])<=0.10 or abs(row['zscore'])>4 or (row1['day']!=row['day'])):
            
            z=(-buy + sell) + (row['lead_close']*trade+row['zinc_close']*-1*trade)
            buy=0
            sell=0
            trade=0
        if row['zscore'] <=-1 and trade==0:
            
            trade=1
            buy=row['lead_close']
            sell=row['zinc_close']
        if row['zscore']>=1 and trade==0:
            trade=-1
            buy=row['zinc_close']
            sell=row['lead_close']
        if (row1['day']!=row['day']):
            trade=0
            #z=(-buy + sell) + (row['lead_close']*trade+row['zinc_close']*-1*trade)
        pair.loc[i,['return']]=y+z
        pair.loc[i,['position']]=trade
        pair.loc[i,['pnl']]=z/(row['lead_close']+row['zinc_close']) + rowpre['pnl']
        
        y=z+y
        
    return pair.dropna()
ans=market_signals(test)
ans['pnl']=ans['pnl']*100
ans['pnl'][:-1].plot()
ans.iloc[-2]['pnl']
lookbacks = range(2, 40, 5)
returns=[]
for i in lookbacks:
    sf=zscore(test.copy(),i)
    sf=market_signals(sf,1,0.1)
    returns.append(sf.iloc[-2]['pnl'])
    plt.plot(lookbacks,returns,'-o')
    test=dfx[-1000:]
    zcore=zscore(test,6)
    xx=market_signals(zcore)
    xx['zscore'] = xx['zscore'].apply(lambda x: '{:.4f}'.format(x))
    xx['pnl']=xx['pnl']*100
    xx['pnl'][:-1].plot()
    xx['zscore'].plot(kind='hist',bins=500)

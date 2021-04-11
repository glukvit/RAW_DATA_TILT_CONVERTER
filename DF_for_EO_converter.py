import pandas as pd

#df2=pd.DataFrame(['DATE','HAE'])
df=pd.read_csv('/home/gluk/EO_CONVERT/ASC/1min/KLYT_2013_04_16months.txt', sep=',', names=['DATE','HAE','HAN','HK2','MIC'])
#df2=df.copy()
HAE=pd.DataFrame({'DATE':df['DATE'],'HAE':df['HAE']})
HAN=pd.DataFrame({'DATE':df['DATE'],'HAN':df['HAN']})
HK2=pd.DataFrame({'DATE':df['DATE'],'HK2':df['HK2']})
HAE.to_csv('/home/gluk/EO_CONVERT/ASC/1min/KLYT_2013_04_06months_HAE.txt', header=None, index=False)
HAN.to_csv('/home/gluk/EO_CONVERT/ASC/1min/KLYT_2013_04_06months_HAN.txt', header=None, index=False)
HK2.to_csv('/home/gluk/EO_CONVERT/ASC/1min/KLYT_2013_04_06months_HK2.txt', header=None, index=False)
print(df2)
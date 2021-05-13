import pandas as pd
import os
from numba import njit

#@njit

def coef(name_fl_in_tmpfs, koeff):
	df=pd.read_csv(name_fl_in_tmpfs)

	df_to_user=pd.DataFrame({'DATE':df['DATE'],'HAE':df['0'], 'HAN':df['1'],'HK2':df['2'], 'MIC':df['3']})
#	df_to_user=pd.DataFrame({'DATE':df['DATE'],'HAE':df['0'], 'HAN':df['1'],'HK2':df['2']}) #КОГДА НЕТ ТРЕТЬЕГО КАНАЛА С МИКРОФОНОМ

	df_to_user['HAE']=df_to_user['HAE']*koeff[0]
	df_to_user['HAN']=df_to_user['HAN']*koeff[1]
	df_to_user['HK2']=df_to_user['HK2']*koeff[2]

	df_to_user['HAE']=df_to_user['HAE'].round(3)
	df_to_user['HAN']=df_to_user['HAN'].round(3)
	df_to_user['HK2']=df_to_user['HK2'].round(3)
	
	os.remove(name_fl_in_tmpfs)

	return(df_to_user)

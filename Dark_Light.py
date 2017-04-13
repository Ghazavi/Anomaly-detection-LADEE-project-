import pandas as pd
import numpy
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
from numpy import median
def Beginning_of_mission_objects(Time,SA):
	return('Nothing')


def Beginning_last_sample(Time,SA):
	for index in range(len(Time)):
		if SA[index]<.05:
			break
		last_sample=index
	return(last_sample)

def Number_of_windows(Start_time,End_time,period):
	return(int((datetime.strptime(End_time, '%y-%j-%H:%M:%S.%f')-datetime.strptime(Start_time, '%y-%j-%H:%M:%S.%f'))/timedelta(hours=period)))

def Beginning_of_window(Start_time,window_number,period):
	return(datetime.strptime(Start_time, '%y-%j-%H:%M:%S.%f')+timedelta(hours=window_number*period))

def index_of_time(Start_time,low_index,high_index,Time):
	Indexes=[low_index,high_index]
	while Indexes[1]-Indexes[0]>1:
		#print((numpy.median(range(Indexes[0],Indexes[1]+1))))
		test=int(numpy.median(range(Indexes[0],Indexes[1]+1)))
		#print(test)
		Time_point=datetime.strptime(Time[int(test)], '%y-%j-%H:%M:%S.%f')
		if Time_point>=Start_time:
			Indexes[1]=test
		if Time_point<=Start_time:
			Indexes[0]=test
		if Time_point==Start_time:
			Indexes[0]=test
			Indexes[1]=test
	if datetime.strptime(Time[Indexes[0]], '%y-%j-%H:%M:%S.%f')==Start_time:
		Indexes[1]=Indexes[0]
	if datetime.strptime(Time[Indexes[1]], '%y-%j-%H:%M:%S.%f')==Start_time:
		Indexes[0]=Indexes[1]
	return(Indexes)


def resampling(Start_time,low_index,high_index,End_time,number_of_samples,Time):
	Delta=(End_time-Start_time)/number_of_samples # sample times
	Start_Indexes=index_of_time(Start_time,low_index,high_index,Time)
	Low_bound_index=Start_Indexes[0]
	End_Indexes=index_of_time(End_time,low_index,high_index,Time)
	High_bound_index=End_Indexes[1]
	Indexes=[Start_Indexes]
	for i in range(1,number_of_samples):
		time_point=Start_time+i*Delta
		Index_point=index_of_time(time_point,Low_bound_index,High_bound_index,Time)
		Low_bound_index=Index_point[0]
		Indexes.append(Index_point)
	return(Indexes)



EPSIO_col_header_name = ['Timestamp',' EPSIO.SA_CURRENT'] #Reading solar array current and timestamp
EPSIO = pd.read_csv('C:/Users/hkhorasgani/Education/RA/LADEE/DataSetComplete/LADEE/Data/EST_SOH.csv/EPSIO.csv', usecols=EPSIO_col_header_name)
Time=EPSIO['Timestamp'].tolist()
SA=EPSIO[' EPSIO.SA_CURRENT'].tolist()
dateparse = lambda x: datetime.strptime(x, '%y-%j-%H:%M:%S.%f')
print(timedelta(hours=1))
print(Number_of_windows(Time[0],Time[Beginning_last_sample(Time,SA)],1))
print(Beginning_of_window(Time[0],0,1))
print(Beginning_of_window(Time[0],4,1))
Indexes=index_of_time(Beginning_of_window(Time[0],4,1),0,len(Time)-1,Time)
print(Indexes)
print(Time[Indexes[0]])
print(Time[Indexes[1]])
print(datetime.strptime(Time[Indexes[0]], '%y-%j-%H:%M:%S.%f'))
print(datetime.strptime(Time[Indexes[1]], '%y-%j-%H:%M:%S.%f'))

Last_index=0
for i in range(2):
	Samples=resampling(Beginning_of_window(Time[0],i,1),0,len(Time)-1,Beginning_of_window(Time[0],i+1,1),15,Time)
	print(Samples)
	




#for index in range(len(Time)):
	#print(Time[index])
	#if SA[index]>.1:
		#print('Light')
	#else:
		#print('Dark')
#print(list(map(lambda x: pd.datetime.strptime(x, '%y-%j-%H:%M:%S.%f'), EPSIO['Timestamp'].tolist())))
import pandas as pd
import numpy
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
from numpy import median
#import math

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
	Set_of_Time_Points=[Start_time]
	for i in range(1,number_of_samples-1):
		time_point=Start_time+i*Delta
		Set_of_Time_Points.append(time_point)
		Index_point=index_of_time(time_point,Low_bound_index,High_bound_index,Time)
		Low_bound_index=Index_point[0]
		Indexes.append(Index_point)
	return(Indexes, Set_of_Time_Points)

def values_of_samples(samples, Set_of_Time_Points,Time,Feature):
	value=[]
	for  i in range(len(samples)):
		if samples[i][0]==samples[i][1]:
			value.append(Feature[samples[i][0]])
		else:
			a=1-(Set_of_Time_Points[i]-datetime.strptime(Time[samples[i][0]], '%y-%j-%H:%M:%S.%f'))/(datetime.strptime(Time[samples[i][1]], '%y-%j-%H:%M:%S.%f')-datetime.strptime(Time[samples[i][0]], '%y-%j-%H:%M:%S.%f'))
			b=1-(datetime.strptime(Time[samples[i][1]], '%y-%j-%H:%M:%S.%f')-Set_of_Time_Points[i])/(datetime.strptime(Time[samples[i][1]], '%y-%j-%H:%M:%S.%f')-datetime.strptime(Time[samples[i][0]], '%y-%j-%H:%M:%S.%f'))
			#print(a)
			#print(Feature[samples[i][0]])
			#print(b)
			#print(Feature[samples[i][1]])
			value.append((Feature[samples[i][0]]*a)+(Feature[samples[i][1]]*b))
	return(value)


def Wavelet_finction_haar(values_of_samples,level):
	low_pass_filter=[1/2**(.5), 1/2**(.5)]
	high_pass_filter=[-1/2**(.5), 1/2**(.5)]
	#print(low_pass_filter)
	#print(high_pass_filter)
	#print(values_of_samples)
	#print('####################################################################')
	#print(numpy.convolve(values_of_samples, low_pass_filter, mode='full')[1::2])
	#print(numpy.convolve(values_of_samples, high_pass_filter, mode='full')[1::2])
	low_pass_coefficients=values_of_samples
	for i in range(level-1):
		low_pass_coefficients= numpy.convolve(low_pass_coefficients, low_pass_filter, mode='full')[1::2]
	high_pass_coefficients= numpy.convolve(low_pass_coefficients, high_pass_filter, mode='full')[1::2]
	low_pass_coefficients= numpy.convolve(low_pass_coefficients, low_pass_filter, mode='full')[1::2]
	return(low_pass_coefficients,high_pass_coefficients)


def Standardization(data,features):
	standardized_data=data
	for x in features:
		if min(data[x])==max(data[x]):
			standardized_data[x]=data[x]-min(data[x])
			print(x,'is a constant variable')
		else:
			standardized_data[x]=(data[x]-min(data[x]))/(max(data[x])-min(data[x]))
	return(standardized_data)








def Objects(subsystems,feature_set,Start_time,End_time,period,number_of_samples_per_window,wave_let_level):
	number_of_windows=Number_of_windows(Start_time,End_time,period)
	#print(number_of_windows)
	number_of_wavelet_coefficients=number_of_samples_per_window/(2**wave_let_level)
	number_of_features=numpy.sum(numpy.array([len(x) for x in feature_set]))	
	#print('num1',number_of_features)
	Object_Set=numpy.zeros((int(number_of_windows),int(number_of_features),int(number_of_wavelet_coefficients*2)))
	feature_index=0
	for i in range(len(subsystems)):
		address='C:/Users/hkhorasgani/Education/RA/LADEE/DataSetComplete/LADEE/Data/EST_SOH.csv/'+ subsystems[i] +'.csv'
		#print(feature_set[i])
		Data = pd.read_csv(address, usecols=feature_set[i])
		Data=Standardization(Data,feature_set[i])
		Data_Time = pd.read_csv(address, usecols=['Timestamp'])
		Time=Data_Time['Timestamp'].tolist()
		#print(len(Time))
		for j in range(number_of_windows):
			Samples_indexes, Samples_times =resampling(Beginning_of_window(Start_time,j,1),0,len(Time)-1,Beginning_of_window(Start_time,j+1,1),number_of_samples_per_window,Time)
			for k in range(len(feature_set[i])):
				Feature=Data[feature_set[i][k]].tolist()
				low_pass_coefficients,high_pass_coefficients=Wavelet_finction_haar(values_of_samples(Samples_indexes, Samples_times,Time,Feature),wave_let_level)
				#print(low_pass_coefficients)
				for l in range(len(low_pass_coefficients)):
					Object_Set[j][feature_index+k][l]=low_pass_coefficients[l]
					#print(l)
					Object_Set[j][feature_index+k][int(number_of_wavelet_coefficients)+l]=high_pass_coefficients[l]
					#print(int(number_of_wavelet_coefficients)+l)
					#print(int(number_of_wavelet_coefficients*2))
				#print(Object_Set[j][feature_index+k])
			#print(Object_Set[j])
		feature_index=feature_index+len(feature_set[i])
	print(Object_Set[5])
				#print('Low passs', low_pass_coefficients)
				#print('High passs', high_pass_coefficients)
	return(Object_Set)









RWIO_col_header_name = ['Timestamp',
' RWIO.EST_RWH_BODY_TRQ[0]',
' RWIO.EST_RWH_BODY_TRQ[1]',
' RWIO.EST_RWH_BODY_TRQ[2]',
' RWIO.EST_RWH_BODY_TRQ[3]',
' RWIO.EST_WHL_SPEED[0]',
' RWIO.EST_WHL_SPEED[1]',
' RWIO.EST_WHL_SPEED[2]',
' RWIO.EST_WHL_SPEED[3]',
' RWIO.TEMP_GYRO[0]',
' RWIO.TEMP_GYRO[1]',
' RWIO.TEMP_GYRO[2]',
' RWIO.TEMP_GYRO[3]',
' RWIO.TEMP_MOTOR[0]',
' RWIO.TEMP_MOTOR[1]',
' RWIO.TEMP_MOTOR[2]',
' RWIO.TEMP_MOTOR[3]',
' RWIO.RATE_COARSE[0]',
' RWIO.RATE_COARSE[1]',
' RWIO.RATE_COARSE[2]',
' RWIO.RATE_COARSE[3]',
' RWIO.GYRO_COARSE[0]',
' RWIO.GYRO_COARSE[1]',
' RWIO.GYRO_COARSE[2]',
' RWIO.GYRO_COARSE[3]']
#RWIO = pd.read_csv('C:/Users/hkhorasgani/Education/RA/LADEE/DataSetComplete/LADEE/Data/EST_SOH.csv/RWIO.csv', usecols=RWIO_col_header_name)

EPSIO_col_header_name = ['Timestamp',' EPSIO.SA_CURRENT'] #Reading solar array current and timestamp
EPSIO = pd.read_csv('C:/Users/hkhorasgani/Education/RA/LADEE/DataSetComplete/LADEE/Data/EST_SOH.csv/EPSIO.csv', usecols=EPSIO_col_header_name)
Time=EPSIO['Timestamp'].tolist()
SA=EPSIO[' EPSIO.SA_CURRENT'].tolist()
dateparse = lambda x: datetime.strptime(x, '%y-%j-%H:%M:%S.%f')
#print(timedelta(hours=1))
#print(Number_of_windows(Time[0],Time[Beginning_last_sample(Time,SA)],1))
#print(Beginning_of_window(Time[0],0,1))
#print(Beginning_of_window(Time[0],4,1))
Indexes=index_of_time(Beginning_of_window(Time[0],4,1),0,len(Time)-1,Time)
#print(Indexes)
#print(Time[Indexes[0]])
#print(Time[Indexes[1]])
#print(datetime.strptime(Time[Indexes[0]], '%y-%j-%H:%M:%S.%f'))
#print(datetime.strptime(Time[Indexes[1]], '%y-%j-%H:%M:%S.%f'))

Last_index=0
for i in range(1):
	Samples_indexes, Samples_times =resampling(Beginning_of_window(Time[0],i,1),0,len(Time)-1,Beginning_of_window(Time[0],i+1,1),16,Time)
	#print(Samples_times)
	#print(values_of_samples(Samples_indexes, Samples_times,Time,SA))
	level=4
	low_pass_coefficients,high_pass_coefficients=Wavelet_finction_haar(values_of_samples(Samples_indexes, Samples_times,Time,SA),level)
	#print(low_pass_coefficients)
	#print(high_pass_coefficients)
subsystems=['RWIO', 'EPSIO', 'IMUIO']
feature_set=[[' RWIO.EST_RWH_BODY_TRQ[0]',
' RWIO.EST_RWH_BODY_TRQ[1]',
' RWIO.EST_RWH_BODY_TRQ[2]',
' RWIO.EST_RWH_BODY_TRQ[3]'],[' EPSIO.SA_CURRENT'],[' IMUIO.P_IMU_PROP_ACC0']]
#Objects(subsystems)
print(Time[0])
print(Time[10000])
print('Hi')
Objects(subsystems,feature_set,Time[0],Time[10000],1,64,4)	



#for index in range(len(Time)):
	#print(Time[index])
	#if SA[index]>.1:
		#print('Light')
	#else:
		#print('Dark')
#print(list(map(lambda x: pd.datetime.strptime(x, '%y-%j-%H:%M:%S.%f'), EPSIO['Timestamp'].tolist())))
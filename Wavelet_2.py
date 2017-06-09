def Number_of_windows(Start_time,End_time,period):
	return(int((datetime.strptime(End_time, '%y-%j-%H:%M:%S.%f')-datetime.strptime(Start_time, '%y-%j-%H:%M:%S.%f'))/timedelta(hours=period)))

def Wavelet_finction_haar(values_of_samples,level):
	low_pass_filter=[1/2**(.5), 1/2**(.5)]
	high_pass_filter=[1/2**(.5), -1/2**(.5)]
	low_pass_coefficients=values_of_samples
	for i in range(level-1):
		low_pass_coefficients= numpy.convolve(low_pass_coefficients, low_pass_filter, mode='full')[1::2]
	high_pass_coefficients= numpy.convolve(low_pass_coefficients, high_pass_filter, mode='full')[1::2]
	low_pass_coefficients= numpy.convolve(low_pass_coefficients, low_pass_filter, mode='full')[1::2]
	return(low_pass_coefficients,high_pass_coefficients)

def wavelet_coefficients(Data,DWT_level,number_of_samples_per_window,number_of_windows,feature_set):
	number_of_wavelet_coefficients=number_of_samples_per_window/(2**DWT_level)
	number_of_features=Data.shape[1]-2
	print(number_of_features)
	print(number_of_wavelet_coefficients)
	wavelet_coef=numpy.zeros((int(number_of_windows),number_of_features*2*int(number_of_wavelet_coefficients)))
	Features_names=['object number']+[item for sublist in feature_set for item in sublist ]
	for i in range(1,Data.shape[1]-1):
		Feature=Data[Features_names[i]]
		for j in range(number_of_windows):
			x=Feature[j*number_of_samples_per_window:((j+1)*number_of_samples_per_window)]
			low_pass_coefficients,high_pass_coefficients=Wavelet_finction_haar(x,DWT_level)
			#print('low_pass_coefficients', low_pass_coefficients)
			#print('high_pass_coefficients', high_pass_coefficients)
			coeffs = pywt.wavedec(x, 'haar', level=DWT_level)
			cA4 ,cD4, cD3, cD2, cD1 = coeffs
			print('cD4-high_pass_coefficients', cD4-high_pass_coefficients)
			print('cA4-low_pass_coefficients', cA4-low_pass_coefficients)
			for k in range(len(low_pass_coefficients)):
				wavelet_coef[j,(i-1)*int(number_of_wavelet_coefficients)*2+k]=low_pass_coefficients[k]
				wavelet_coef[j,(i-1)*int(number_of_wavelet_coefficients)*2+k+len(low_pass_coefficients)]=high_pass_coefficients[k]
	return(wavelet_coef)

def Read_data(subsystem,feature_set):
	#Data address
	address='C:/Users/hkhorasgani/Education/RA/LADEE/Resampling/'+ subsystem +'.csv'
	features=['Timestamp']+feature_set #Adding time to the list of features 
	Data = pd.read_csv(address, usecols=features)
	return(Data)

def Last_start_time_subsystems(subsystems):
	start_point=datetime.strptime('12-250-11:34:54.059', '%y-%j-%H:%M:%S.%f')
	features=[]
	for subsystem in subsystems:
		Data=Read_data(subsystem,features)
		time=Data['Timestamp'].tolist()
		start_time=time[0]
		if datetime.strptime(start_time, '%y-%j-%H:%M:%S.%f')>start_point:
			start_point=datetime.strptime(start_time, '%y-%j-%H:%M:%S.%f')
			Latest_time=start_time
	return(Latest_time)

def First_end_time_subsystems(subsystems):
	end_point=datetime.strptime('17-250-11:34:54.059', '%y-%j-%H:%M:%S.%f')
	features=[]
	for subsystem in subsystems:
		Data=Read_data(subsystem,features)
		time=Data['Timestamp'].tolist()
		end_time=time[-1]
		if datetime.strptime(end_time, '%y-%j-%H:%M:%S.%f')<end_point:
			end_point=datetime.strptime(end_time, '%y-%j-%H:%M:%S.%f')
	return(end_point)

def Modify_the_light_dark_file(Dark_light_time,end_time):
	dateparse1 = lambda x: pd.datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ')
	for i in range(len(Dark_light_time)):
		if dateparse1(Dark_light_time[i])>end_time:
			print(Dark_light_time[i])
			break
			#time.remove(Dark_light_time[i])
	time=Dark_light_time[0:i-1]
	print(time[-1])
	return(time)


if __name__=='__main__':
	import pandas as pd
	import numpy
	from datetime import date
	from datetime import time
	from datetime import datetime
	from datetime import timedelta
	import time
	import variables
	import pywt
	feature_set=variables.feature_set
	subsystems=variables.subsystems
	address='C:/Users/hkhorasgani/Education/RA/LADEE/DataSetComplete/LADEE/Data/EST_SOH.csv/EPSIO.csv'
	Data_Time = pd.read_csv(address, usecols=['Timestamp'])
	Time=Data_Time['Timestamp'] .tolist()
	Start_time=Last_start_time_subsystems(subsystems)
	End_time=Time[171245]
	samples_per_window=64
	DWT_level=4
	period=1
	Data= pd.read_csv('Resample_Data.csv')
	number_of_windows=Number_of_windows(Start_time,End_time,period)
	wavelet_coef=wavelet_coefficients(Data,DWT_level,samples_per_window,number_of_windows,feature_set)
	df = pd.DataFrame(wavelet_coef)
	df.to_csv("wavelet_coef.csv", index=False ) 



	address2='C:/Users/hkhorasgani/Education/RA/LADEE/Resampling/out.csv'
	dateparse2 = lambda x: pd.datetime.strptime(x, '%y-%j-%H:%M:%S.%f')
	Dark_light=pd.read_csv(address2)
	Dark_light_time=Dark_light['timestamp'].tolist()
	end_time=First_end_time_subsystems(subsystems)
	Dark_light_time_points=Modify_the_light_dark_file(Dark_light_time,end_time)
	number_of_windows_2=len(Dark_light_time_points)-1
	Data_2= pd.read_csv('Resample_Data_2.csv')
	wavelet_coef_2=wavelet_coefficients(Data_2,DWT_level,samples_per_window,number_of_windows_2,feature_set)
	df = pd.DataFrame(wavelet_coef_2)
	df.to_csv("wavelet_coef_2.csv", index=False ) 
	
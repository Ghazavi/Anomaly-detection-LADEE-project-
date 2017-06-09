def Read_data(subsystem,feature_set):
	#Data address
	address='C:/Users/hkhorasgani/Education/RA/LADEE/Resampling/'+ subsystem +'.csv'
	features=['Timestamp']+feature_set #Adding time to the list of features 
	Data = pd.read_csv(address, usecols=features)
	return(Data)

def Number_of_windows(Start_time,End_time,period):
	return(int((datetime.strptime(End_time, '%y-%j-%H:%M:%S.%f')-datetime.strptime(Start_time, '%y-%j-%H:%M:%S.%f'))/timedelta(hours=period)))

def Beginning_of_window(Start_time,window_number,period):
	return(datetime.strptime(Start_time, '%y-%j-%H:%M:%S.%f')+timedelta(hours=window_number*period))


def index_of_time(Start_time,low_index,high_index,Time):
	Indexes=[low_index,high_index]
	while Indexes[1]-Indexes[0]>1:
		test=int(numpy.median(range(Indexes[0],Indexes[1]+1)))
		Time_point=datetime.strptime(Time[int(test)], '%y-%j-%H:%M:%S.%f')
		if Time_point>=Start_time:
			Indexes[1]=test
		if Time_point<=Start_time:
			Indexes[0]=test
		if Time_point==Start_time:
			Indexes[0]=test
			Indexes[1]=test
		if Indexes[0]!=Indexes[1]:
			Beginning_time=datetime.strptime(Time[int(Indexes[0])], '%y-%j-%H:%M:%S.%f')
			End_time=datetime.strptime(Time[int(Indexes[1])], '%y-%j-%H:%M:%S.%f')
			test2=int(Indexes[0]+math.ceil(((Start_time-Beginning_time)/(End_time-Beginning_time))*(Indexes[1]-Indexes[0])))
			Time_point2=datetime.strptime(Time[int(test2)], '%y-%j-%H:%M:%S.%f')
			if Time_point2>=Start_time and Time_point2<End_time:
				Indexes[1]=test2
			if Time_point2<=Start_time and Time_point2>Beginning_time:
				Indexes[0]=test2
			if Time_point2==Start_time:
				Indexes[0]=test2
				Indexes[1]=test2
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
	for i in range(1,number_of_samples):
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
			if a>1 or b>1 or a<0 or b<0:
				print('a',a)
				print('b',b)
			value.append((Feature[samples[i][0]]*a)+(Feature[samples[i][1]]*b))
			if (((Feature[samples[i][0]]*a)+(Feature[samples[i][1]]*b))>1):
				print('a',a)
				print('b',b)
				print(Feature[samples[i][0]])
				print(Feature[samples[i][1]])
	return(value)

def Resampling_Data(subsystems,feature_set,Start_time,End_time,period,number_of_samples_per_window):
	number_of_windows=Number_of_windows(Start_time,End_time,period)
	number_of_features=numpy.sum(numpy.array([len(x) for x in feature_set]))
	print(number_of_features)
	Object_Set=numpy.zeros((int(number_of_windows)*number_of_samples_per_window,int(number_of_features)+1))
	feature_index=1
	test_Data=list()
	for i in range(len(subsystems)):
		Data=Read_data(subsystems[i],feature_set[i])
		Time=Data['Timestamp'] .tolist()
		for j in range(number_of_windows):
			Samples_indexes, Samples_times =resampling(Beginning_of_window(Start_time,j,period),0,len(Time)-1,Beginning_of_window(Start_time,j+1,period),number_of_samples_per_window,Time)
			for k in range(len(feature_set[i])):
				Feature=Data[feature_set[i][k]]
				Feature_values=values_of_samples(Samples_indexes, Samples_times,Time,Feature)
				for l in range(len(Feature_values)):
					Object_Set[j*number_of_samples_per_window+l][feature_index+k]=Feature_values[l]
					Object_Set[j*number_of_samples_per_window+l][0]=j
					#test_Data[j*number_of_samples_per_window+l]={'Time':Samples_times[l]}
		feature_index=feature_index+len(feature_set[i])	
		print(feature_index)
	Features_names=['object number']+[item for sublist in feature_set for item in sublist ]
	df = pd.DataFrame(Object_Set, columns = Features_names)
	df.to_csv("Resample_Data.csv")
	time_of_objects=[]
	for j in range(number_of_windows):
		time_of_objects.append(Beginning_of_window(Start_time,j,period))
	time_df = pd.DataFrame(time_of_objects, columns = ['start time'])
	time_df.to_csv("Start_time.csv")
	return(Object_Set)
					
		#print(len(Time))
		#print(Time[0:10])

def Resampling_Data_2(subsystems,feature_set,number_of_samples_per_window,Dark_light_time):
	#number_of_windows=Number_of_windows(Start_time,End_time,period)
	number_of_windows=len(Dark_light_time)-1
	print(number_of_windows)
	number_of_features=numpy.sum(numpy.array([len(x) for x in feature_set]))
	dateparse1 = lambda x: pd.datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ')
	Object_Set=numpy.zeros((int(number_of_windows)*number_of_samples_per_window,int(number_of_features)+1))
	feature_index=1
	test_Data=list()
	for i in range(len(subsystems)):
		Data=Read_data(subsystems[i],feature_set[i])
		Time=Data['Timestamp'] .tolist()
		for j in range(number_of_windows):
			Samples_indexes, Samples_times =resampling(dateparse1(Dark_light_time[j]),0,len(Time)-1,dateparse1(Dark_light_time[j+1]),number_of_samples_per_window,Time)
			for k in range(len(feature_set[i])):
				Feature=Data[feature_set[i][k]]
				Feature_values=values_of_samples(Samples_indexes, Samples_times,Time,Feature)
				for l in range(len(Feature_values)):
					Object_Set[j*number_of_samples_per_window+l][feature_index+k]=Feature_values[l]
					Object_Set[j*number_of_samples_per_window+l][0]=j
					#test_Data[j*number_of_samples_per_window+l]={'Time':Samples_times[l]}
		feature_index=feature_index+len(feature_set[i])	
		print(feature_index)
	Features_names=['object number']+[item for sublist in feature_set for item in sublist ]
	df = pd.DataFrame(Object_Set, columns = Features_names)
	df.to_csv("Resample_Data_2.csv")
	time_of_objects=[]
	for j in range(number_of_windows):
		time_of_objects.append(dateparse1(Dark_light_time[j]))
	time_df = pd.DataFrame(time_of_objects, columns = ['start time'])
	time_df.to_csv("Start_time_2.csv")
	return(Object_Set)


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
	import pandas as pd
	import numpy
	from datetime import date
	from datetime import time
	from datetime import datetime
	from datetime import timedelta
	import time
	import math
	import variables
	feature_set=variables.feature_set
	subsystems=variables.subsystems
	#from variables import EPSIO_Features
	#Data=Read_data(subsytems[0],set_of_features[0])
	
	address='C:/Users/hkhorasgani/Education/RA/LADEE/DataSetComplete/LADEE/Data/EST_SOH.csv/EPSIO.csv'
	Data_Time = pd.read_csv(address, usecols=['Timestamp'])
	Time=Data_Time['Timestamp'] .tolist()
	Start_time=Time[0]
	print(Start_time)
	Start_time=Last_start_time_subsystems(subsystems)
	print(Start_time)
	End_time=Time[171245]
	number_of_samples_per_window=64
	period=1
	Resampling_Data(subsystems,feature_set,Start_time,End_time,period,number_of_samples_per_window)





	address2='C:/Users/hkhorasgani/Education/RA/LADEE/Resampling/out.csv'
	dateparse2 = lambda x: pd.datetime.strptime(x, '%y-%j-%H:%M:%S.%f')
	Dark_light=pd.read_csv(address2)
	Dark_light_time=Dark_light['timestamp'].tolist()
	end_time=First_end_time_subsystems(subsystems)
	Dark_light_time_points=Modify_the_light_dark_file(Dark_light_time,end_time)
	Resampling_Data_2(subsystems,feature_set,number_of_samples_per_window,Dark_light_time_points)
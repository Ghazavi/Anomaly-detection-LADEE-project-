def Read_data(subsystem,feature_set):
	#Data address
	address='C:/Users/hkhorasgani/Education/RA/LADEE/DataSetComplete/LADEE/Data/EST_SOH.csv/'+ subsystem +'.csv'
	features=['Timestamp']+feature_set #Adding time to the list of features 
	Data = pd.read_csv(address, usecols=features)
	return(Data)


def Standardization(data,features):
	standardized_data=data
	for x in features:
		if min(data[x])==max(data[x]):
			standardized_data[x]=data[x]-min(data[x])
			print(x,'is a constant variable')
			standardized_data[x]=data[x]-min(data[x])
		else:
			standardized_data[x]=(data[x]-min(data[x]))/(max(data[x])-min(data[x]))
	return(standardized_data)




if __name__=='__main__':
	import pandas as pd
	import variables
	for i in range(len(variables.subsystems)):
		name_of_data=variables.subsystems[i]
		features=variables.feature_set[i]
		Data=Read_data(name_of_data,features)
		Standardize_Data=Standardization(Data,features)
		Standardize_Data.to_csv(name_of_data+".csv", index=False ) 



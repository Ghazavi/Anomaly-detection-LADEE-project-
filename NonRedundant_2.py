def Feature_names(feature_set,number_of_samples_per_window,wave_let_level):
	number_of_wavelet_coefficients=number_of_samples_per_window/(2**wave_let_level)
	#print(number_of_wavelet_coefficients)
	Feature_name_list=[]
	Features=[item for sublist in feature_set for item in sublist ]
	for x in Features:
		for i in range(int(number_of_wavelet_coefficients)):
			Feature_name_list.append(''.join((x,'low',str(i))))
		for i in range(int(number_of_wavelet_coefficients)):
			Feature_name_list.append(''.join((x,'high',str(i))))
	return(Feature_name_list)

def Select_Non_Redundant_Features(data,Non_Redundant_Features,Non_Redundant_indexes):
	selected_coef=numpy.zeros((int(len(data)),len(Non_Redundant_Features)))
	for i in range(len(Non_Redundant_indexes)):
		for j in range(len(data)):
			selected_coef[j,i]=data[j,Non_Redundant_indexes[i]]
	df = pd.DataFrame(selected_coef,columns = Non_Redundant_Features)
	df.to_csv("Non_Redundant_coef.csv", index=False )
	return(selected_coef) 

def Select_Non_Redundant_Features_2(data,Non_Redundant_Features,Non_Redundant_indexes):
	selected_coef=numpy.zeros((int(len(data)),len(Non_Redundant_Features)))
	for i in range(len(Non_Redundant_indexes)):
		for j in range(len(data)):
			selected_coef[j,i]=data[j,Non_Redundant_indexes[i]]
	df = pd.DataFrame(selected_coef,columns = Non_Redundant_Features)
	df.to_csv("Non_Redundant_coef_2.csv", index=False )
	return(selected_coef) 


def Redundant_variables(X_Data,threshold):
	#number=numpy.zeros((X_Data.shape[1],1))
	redundant_variables=[]
	for i in range(X_Data.shape[1]):
		for j in range(i,X_Data.shape[1]):
			if i!=j:
				x=X_Data[:,i]
				y=X_Data[:,j]
				score=pearsonr(x,y)
				if score[0]>=threshold:
					#number[i]=number[i]+1
					redundant_variables.append(j)
					print(i,j,Features_all[i],Features_all[j],score[0])
	print(len(set(redundant_variables)))
	return(redundant_variables)

def Non_Redundant_Features(redundants,Features_all):
	Non_Redundants=[]
	for i in range(len(Features_all)):
		if i  not in redundants:
			Non_Redundants.append(Features_all[i])
	return(Non_Redundants)

def Non_Redundant_indexes(redundants,Features_all):
	Non_Redundants=[]
	for i in range(len(Features_all)):
		if i  not in redundants:
			Non_Redundants.append(i)
	return(Non_Redundants)  

if __name__=='__main__':
	import operator 
	import numpy
	import pandas as pd
	import math
	from variables import feature_set
	from scipy.cluster.hierarchy import dendrogram, linkage
	from scipy.cluster.hierarchy import cophenet
	from scipy.spatial.distance import pdist
	from scipy.cluster.hierarchy import fcluster
	from scipy.stats.stats import pearsonr 
	import matplotlib.pylab as plt
	import variables

	#Exracting the set of features
	number_of_samples_per_window=64
	wave_let_level=4
	Features_all=Feature_names(feature_set,number_of_samples_per_window,wave_let_level)


	#Laplacian scores
	data = pd.read_csv('wavelet_coef.csv')
	X_Data = data.as_matrix().astype("float32", copy = False)
	print(X_Data.shape)
	threshold=.99
	

	redundants=Redundant_variables(X_Data,threshold)
	No_Redundant_Features=Non_Redundant_Features(redundants,Features_all)
	No_Redundant_indexes=Non_Redundant_indexes(redundants,Features_all)
	print(len(No_Redundant_indexes))	
	print(len(No_Redundant_indexes))
	Select_Non_Redundant_Features(X_Data,No_Redundant_Features,No_Redundant_indexes)



	data = pd.read_csv('wavelet_coef_2.csv')
	X_Data = data.as_matrix().astype("float32", copy = False)
	print(X_Data.shape)
	

	redundants=Redundant_variables(X_Data,threshold)
	No_Redundant_Features=Non_Redundant_Features(redundants,Features_all)
	No_Redundant_indexes=Non_Redundant_indexes(redundants,Features_all)
	print(len(No_Redundant_indexes))	
	print(len(No_Redundant_indexes))
	Select_Non_Redundant_Features_2(X_Data,No_Redundant_Features,No_Redundant_indexes)




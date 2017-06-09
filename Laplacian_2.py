def euclideanDistance(Object_1,Object_2):
	return((numpy.sum((numpy.array(Object_1)-numpy.array(Object_2))**2))**(.5))


def getNeighbors(trainingSet, testInstance, k, distance_function):
	distances = []
	for x in range(len(trainingSet)):
		dist = distance_function(testInstance, trainingSet[x])
		distances.append((x, dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return(neighbors)

def S_matrix(trainingSet,k,distance_function,t):
	S=numpy.zeros((int(trainingSet.shape[0]),int(trainingSet.shape[0])))
	for i in range(len(trainingSet)):
		neighbors=getNeighbors(trainingSet, trainingSet[i], k, distance_function)
		for j in range(k):
			dist = distance_function(trainingSet[i], trainingSet[neighbors[j]])
			S[i][neighbors[j]]=math.exp(-pow(dist,2)/t)
	return(S)

def D_matrix(S_matrix):
	I_vector=numpy.ones(int(S_matrix.shape[0]))
	#print(I_vector.shape)
	D=numpy.diag(numpy.dot(S_matrix,I_vector))
	#print(D.shape)
	return(D)

def Normalized_feature(feature,D_matrix):
	I_vector=numpy.ones(int(D_matrix.shape[0]))
	#print(I_vector.shape)
	#print(feature.shape)
	normalized_feature=feature-((numpy.dot(numpy.array(feature), numpy.dot(D_matrix,I_vector)))/(numpy.dot(I_vector, numpy.dot(D_matrix,I_vector))))*I_vector
	return(normalized_feature)

def Laplacian_Score(L_matrix,D_matrix,normalized_feature):
	L_r = numpy.dot(numpy.array(normalized_feature), numpy.dot(L_matrix,numpy.array(normalized_feature)))/numpy.dot(numpy.array(normalized_feature), numpy.dot(D_matrix,numpy.array(normalized_feature)))
	#if numpy.dot(numpy.array(normalized_feature), numpy.dot(L_matrix,numpy.array(normalized_feature)))<0:
	#print(numpy.dot(numpy.array(normalized_feature), numpy.dot(L_matrix,numpy.array(normalized_feature))))
	return(L_r)
	
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

def find_indexes_of_groups(groups,group_number):
	index_of_group=[]
	for i in range(len(groups)):
		if groups[i]==group_number:
			index_of_group.append(i)
	return(index_of_group)


def distance_structure(X_Data):
	Data_strucutre=numpy.zeros((int(X_Data.shape[0]),int(X_Data.shape[0])))
	for i in range(X_Data.shape[0]):
		for j in range(X_Data.shape[0]):
			Data_strucutre[i][j]=euclideanDistance(X_Data[i,:],X_Data[j,:])
	return(Data_strucutre.flatten())

def distance_feature(Data_feature):
	#print(len(Data_feature))
	Data_strucutre=numpy.zeros((len(Data_feature),len(Data_feature)))
	for i in range(len(Data_feature)):
		for j in range(len(Data_feature)):
			Data_strucutre[i][j]=abs(Data_feature[i]-Data_feature[j])
	return(Data_strucutre.flatten())

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

def Select_Features(data,X_Data,Laplacian_Scores,Number_of_selected_features):
	indexes=[i[0] for i in sorted(enumerate(Laplacian_Scores), key=lambda x:x[1])]
	selected_coef=numpy.zeros((int(len(data)),Number_of_selected_features))
	Features=data.columns.values.tolist()
	headers=[]
	for i in range(Number_of_selected_features):
		headers.append(Features[indexes[i]])
		print(Features[indexes[i]])
		for j in range(len(data)):
			selected_coef[j,i]=X_Data[j,indexes[i]]
	df = pd.DataFrame(selected_coef,columns = headers)
	df.to_csv("selected_coef.csv", index=False )
	return(selected_coef) 

def Select_Features_2(data,X_Data,Laplacian_Scores,Number_of_selected_features):
	indexes=[i[0] for i in sorted(enumerate(Laplacian_Scores), key=lambda x:x[1])]
	selected_coef=numpy.zeros((int(len(data)),Number_of_selected_features))
	Features=data.columns.values.tolist()
	headers=[]
	for i in range(Number_of_selected_features):
		headers.append(Features[indexes[i]])
		print(Features[indexes[i]])
		for j in range(len(data)):
			selected_coef[j,i]=X_Data[j,indexes[i]]
	df = pd.DataFrame(selected_coef,columns = headers)
	df.to_csv("selected_coef_2.csv", index=False )
	return(selected_coef) 


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
	data = pd.read_csv('Non_Redundant_coef.csv')
	X_Data = data.as_matrix().astype("float32", copy = False)
	print(X_Data.shape)
	S=S_matrix(X_Data,20,euclideanDistance,10)
	D=D_matrix(S)
	L=D-S
	Laplacian_Scores=[]
	for i in range(X_Data.shape[1]):
		normalized_feature=Normalized_feature(X_Data[:,i],D)
		Laplacian_Scores.append(abs(Laplacian_Score(L,D,normalized_feature)))

	

	#Selecting features 
	Number_of_selected_features=100
	selected_data=Select_Features(data,X_Data,Laplacian_Scores,Number_of_selected_features)



	#Laplacian scores
	Number_of_selected_features=200
	data = pd.read_csv('Non_Redundant_coef_2.csv')
	X_Data = data.as_matrix().astype("float32", copy = False)
	print(X_Data.shape)
	S=S_matrix(X_Data,20,euclideanDistance,10)
	D=D_matrix(S)
	L=D-S
	Laplacian_Scores=[]
	for i in range(X_Data.shape[1]):
		normalized_feature=Normalized_feature(X_Data[:,i],D)
		Laplacian_Scores.append(abs(Laplacian_Score(L,D,normalized_feature)))

	

	#Selecting features 
	selected_data=Select_Features_2(data,X_Data,Laplacian_Scores,Number_of_selected_features)

	



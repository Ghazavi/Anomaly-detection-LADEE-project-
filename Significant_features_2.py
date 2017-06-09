def Significant_features(data,groups,normal_group,outlier,threshold):
	dataMatrix = data.as_matrix()
	g_normal=dataMatrix[np.where(groups == normal_group)[0]][:]
	g_normal_mean=np.mean(g_normal,axis=0)
	g_outlier=dataMatrix[np.where(groups == outlier)[0]][:]
	g_outlier_mean=np.mean(g_outlier,axis=0)
	error=[]
	Total_distance=0
	for k in range(dataMatrix.shape[1]):
		error.append(abs(g_normal_mean[k]-g_outlier_mean[k]))
		Total_distance=Total_distance+pow((g_normal_mean[k]-g_outlier_mean[k]),2)
	#print(Total_distance)
	indexes=[i[0] for i in sorted(enumerate(error), key=lambda x:x[1])]
	indexes.reverse()
	Importance=0
	Importance_vector=[]
	S_features=[]
	for i in range(len(indexes)):
		Importance_vector.append(error[indexes[i]]/pow(Total_distance,.5))
		S_features.append(indexes[i])
		Importance=Importance+pow(error[indexes[i]],2)/Total_distance
		if pow(Importance,.5)>=threshold:
			break
	#print(Importance_vector)
	names=list(data)
	S_features_nmaes=[]
	for j in range(len(S_features)):
		S_features_nmaes.append(names[S_features[j]])
		print(names[S_features[j]])
	plt.bar(range(len(S_features)),Importance_vector)
	plt.xlabel("Significant feature index")
	plt.ylabel("Importance")
	plt.show()
	return(S_features)

def Time_of_group(groups,time,outlier):
	t=time.as_matrix()
	print(t[np.where(groups == outlier)])




if __name__=='__main__':
	import numpy as np
	import pandas as pd
	from scipy.cluster.hierarchy import dendrogram, linkage
	from matplotlib import pyplot as plt
	from scipy.spatial.distance import pdist
	from scipy.cluster.hierarchy import fcluster
	data = pd.read_csv('selected_coef.csv')
	time=pd.read_csv('Start_time.csv')
	Z = linkage(data, 'average')
	number_of_clusters=3
	groups=fcluster(Z, number_of_clusters, criterion='maxclust')
	normal_group=1
	outlier=3
	threshold=.75
	Significant_features(data,groups,normal_group,outlier,threshold)
	Time_of_group(groups,time,outlier)




	data = pd.read_csv('selected_coef_2.csv')
	time=pd.read_csv('Start_time_2.csv')
	Z = linkage(data, 'average')
	number_of_clusters=6
	groups=fcluster(Z, number_of_clusters, criterion='maxclust')
	normal_group=2
	outlier=5
	threshold=.75
	Significant_features(data,groups,normal_group,outlier,threshold)
	Time_of_group(groups,time,outlier)



	
	

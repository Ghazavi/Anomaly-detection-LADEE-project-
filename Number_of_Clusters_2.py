#Number of clusters
# Calinski and Harabasz's method [1]
# CH(g)=(B(g)/(g-1))/(W(g)/(n-g))
#W(g) = \sum _{m=1} ^ {g} \sum_{l=1}^{l_m} (x_{lm}-mean(x_m)) (x_{lm}-mean(x_m))'
#B(g) = \sum _{m=1} ^ {g} n_m (mean(x_m)-mean(x)) (mean(x_m)-mean(x))'
# [1] G. W. Milligan and M. C. Cooper. An examination of procedures for determiningthe number of clusters in a data set. Psychometrica, 50:159{179, 1985.





def B_vector(data,Z,min_num_of_gorups,max_num_of_gorups):
	dataMatrix = data.as_matrix()
	objects_mean=np.mean(dataMatrix,axis=0)
	B_vector=[]
	for k in range(min_num_of_gorups,max_num_of_gorups+1):
		groups=fcluster(Z, k, criterion='maxclust')
		B=0
		for j in range(1,k+1):
			g=dataMatrix[np.where(groups == j)[0]][:]
			g_mean=np.mean(g,axis=0)
			B=B+len(g)*np.dot((g_mean-objects_mean),(g_mean-objects_mean))
		B_vector.append(B)
	print('B',B)
	return(B_vector)


def W_vector(data,Z,min_num_of_gorups,max_num_of_gorups):
	dataMatrix = data.as_matrix()
	W_vector=[]
	for k in range(min_num_of_gorups,max_num_of_gorups+1):
		groups=fcluster(Z, k, criterion='maxclust')
		W=0
		for j in range(1,k+1):
			g=dataMatrix[np.where(groups == j)[0]][:]
			g_mean=np.mean(g,axis=0)
			for i in range(len(g)):
				W=W+np.dot((g_mean-g[i][:]),(g_mean-g[i][:]))
		W_vector.append(W)
	print('W',W)
	return(W_vector)




def CH_vector(data,B_vector,W_vector,min_num_of_gorups,max_num_of_gorups):
	CH_vector=[]
	for k in range(len(B_vector)):
		CH=(B_vector[k]/(min_num_of_gorups+k-1))/(W_vector[k]/(len(data)-min_num_of_gorups-k))
		#print((W_vector[k]/(len(data)-min_num_of_gorups-k)))
		#print('(B_vector[k]/(min_num_of_gorups+k-1))',(B_vector[k]/(min_num_of_gorups+k-1)))
		CH_vector.append(CH)
	Answer=range(min_num_of_gorups,max_num_of_gorups+1)
	print('number of clusters CH',Answer[np.argmax(CH_vector)])
	return(CH_vector)


#Hartigan's method
def Har_vector(data,W_vector,min_num_of_gorups,max_num_of_gorups):
	Har_vector=[]
	for k in range(len(W_vector)-1):
		Har=((W_vector[k]/W_vector[k+1])-1)/(len(data)-min_num_of_gorups-k-1)
		Har_vector.append(Har)
	Answer=range(min_num_of_gorups,max_num_of_gorups+1)
	print('number of clusters Har',Answer[np.argmax(Har_vector)])
	return(Har_vector)




#Krzanowski and Lai's method
def KL_vector(data,W_vector,min_num_of_gorups,max_num_of_gorups):
	KL=[]
	DIFF_vector=[]
	print(data.shape[1])
	p=data.shape[1]
	for k in range(1,len(W_vector)):
		g=min_num_of_gorups+k
		DIFF=pow((g-1),2/p)*W_vector[k-1]-pow((g),2/p)*W_vector[k]
		DIFF_vector.append(DIFF)
	for i in range(len(DIFF_vector)-1):
		KL.append(DIFF_vector[i]/DIFF_vector[i+1])
	Answer=range(min_num_of_gorups,max_num_of_gorups+1)
	print('number of clusters KL',Answer[np.argmax(KL)])
	return(KL)




if __name__=='__main__':
	import numpy as np
	import pandas as pd
	from scipy.cluster.hierarchy import dendrogram, linkage
	from matplotlib import pyplot as plt
	from scipy.spatial.distance import pdist
	from scipy.cluster.hierarchy import fcluster
	data = pd.read_csv('selected_coef.csv')
	Z = linkage(data, 'average')
	
	
	min_num_of_gorups=2
	max_num_of_gorups=50
	B=B_vector(data,Z,min_num_of_gorups,max_num_of_gorups)
	#print(B_vector)
	plt.title('B with maximum groups %d clusters' % max_num_of_gorups)
	plt.plot(B)
	plt.show()
	W=W_vector(data,Z,min_num_of_gorups,max_num_of_gorups)
	plt.title('W with maximum groups %d clusters' % max_num_of_gorups)
	plt.plot(W)
	plt.show()
	CH=CH_vector(data,B,W,min_num_of_gorups,max_num_of_gorups)
	plt.title('CH with maximum groups %d clusters' % max_num_of_gorups)
	plt.plot(CH)
	plt.show()
	Har=Har_vector(data,W,min_num_of_gorups,max_num_of_gorups)
	plt.title('Har with maximum groups %d clusters' % max_num_of_gorups)
	plt.plot(Har)
	plt.show()
	KL=KL_vector(data,W,min_num_of_gorups,max_num_of_gorups)
	plt.title('KL with maximum groups %d clusters' % max_num_of_gorups)
	plt.plot(KL)
	plt.show()
	Answer=range(min_num_of_gorups,max_num_of_gorups+1)
	num_groups=max(Answer[np.argmax(KL)],Answer[np.argmax(CH)])
	groups=fcluster(Z, num_groups, criterion='maxclust')
	print(groups)
	plt.title('hierarchical clustering with %d clusters' % num_groups)
	plt.plot(groups)
	plt.show()

	for i in range(1,num_groups+1):
		print('group=',i)
		print(len(groups[np.where(groups == i)]))


	data = pd.read_csv('selected_coef_2.csv')
	Z = linkage(data, 'average')
	
	
	min_num_of_gorups=2
	max_num_of_gorups=50
	B=B_vector(data,Z,min_num_of_gorups,max_num_of_gorups)
	#print(B_vector)
	plt.title('B with maximum groups %d clusters' % max_num_of_gorups)
	plt.plot(B)
	plt.show()
	W=W_vector(data,Z,min_num_of_gorups,max_num_of_gorups)
	plt.title('W with maximum groups %d clusters' % max_num_of_gorups)
	plt.plot(W)
	plt.show()
	CH=CH_vector(data,B,W,min_num_of_gorups,max_num_of_gorups)
	plt.title('CH with maximum groups %d clusters' % max_num_of_gorups)
	plt.plot(CH)
	plt.show()
	Har=Har_vector(data,W,min_num_of_gorups,max_num_of_gorups)
	plt.title('Har with maximum groups %d clusters' % max_num_of_gorups)
	plt.plot(Har)
	plt.show()
	KL=KL_vector(data,W,min_num_of_gorups,max_num_of_gorups)
	plt.title('KL with maximum groups %d clusters' % max_num_of_gorups)
	plt.plot(KL)
	plt.show()
	Answer=range(min_num_of_gorups,max_num_of_gorups+1)
	num_groups=max(Answer[np.argmax(KL)],Answer[np.argmax(CH)])
	groups=fcluster(Z, num_groups, criterion='maxclust')
	print(groups)
	plt.title('hierarchical clustering with %d clusters' % num_groups)
	plt.plot(groups)
	plt.show()

	for i in range(1,num_groups+1):
		print('group=',i)
		print(len(groups[np.where(groups == i)]))


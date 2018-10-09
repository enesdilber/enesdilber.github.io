
# coding: utf-8

# # 1 Description
# 
# 
# ### Course <span style="color:blue">CEng414 Data Mining</span>
# 
# #### Semester <span style="color:blue">Fall 2017</span>
# 
# #### Content  <span style="color:blue">K-means like sckit-learn</span> 
# 
# #### Notebook Language  <span style="color:blue">python</span> 

# In[1]:


import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt
import random 


# # 2 Data Generation

# In[2]:


def generate_normal(n, mean, mySeed = 0):
    np.random.seed(seed = mySeed)
    
    p = mean.shape[1]
    c = mean.shape[0]
             
    K = rand.multivariate_normal(mean[0], np.identity(p), n).T
    
    if(c == 1):
        return K.T
    
    for i in range(1,c):
        K_new = rand.multivariate_normal(mean[i], np.identity(p), n).T
        K = np.hstack((K, K_new))
       
    return K.T


# 5 different bivariate normal, each size=100 with different means and identitiy var-cov matrix:

# In[3]:


myMean = np.array([[1, 4], 
                   [9, 2],
                   [0, -2],
                   [5, 3],
                   [-2, 3]])
n = 100
myX = generate_normal(n, myMean, mySeed = 108)


# In[4]:


plt.scatter(myX[:,0], myX[:,1])
plt.axis('equal')
plt.show()


# # 3 Initialization

# In[5]:


max_iter = 300 #Algorithm ends even if it does not converge after 300 iterations

def euclidian(a, b): 
    return np.linalg.norm(a-b) #L2-distance calculator for 2 points

N, p = myX.shape #N = Number of observations, p = dimension
n_clusters = 5 #Cluster number


# To find initial $cluster\_centers$ I randomly sample points from $myX$ each size $n\_clusters$. Then I calculate the L2 distances between points and get a criteria such that $criteria = mean(distance)^2-var(distance)$. I repeat this proccess $trial$ times and get the one sample that has largest criteria. With this way my aim is to obtain spreaded $cluster\_centers$ and the magnitude of this spread has low variation.

# In[6]:


def find_initials(n_cluster, X, N, trial, mySeed = 0):
    
    if mySeed!=0:
        np.random.seed(seed = mySeed)

    rs_n_dist = np.math.factorial(n_clusters)/(np.math.factorial(n_clusters-2)*np.math.factorial(2))
    opt_criteria = 0

    for k in range(trial):
        rs = X[np.random.choice(np.arange(N), size=n_clusters, replace=False, p=None)]
        rs_dist = np.zeros(0)

        for i in range(n_clusters-1):
            for j in range((i+1), n_clusters):
                rs_dist = np.append(rs_dist, euclidian(rs[i],rs[j]))

        criteria = (np.power(np.mean(rs_dist),2) - np.var(rs_dist))
        if criteria>opt_criteria:
            opt_criteria = criteria
            cluster_centers = rs
            
    return cluster_centers


# In[7]:


trial = int(np.ceil(np.log2(N)*p)) #a formula for choosing number of trials


# In[8]:


cluster_centers = find_initials(n_clusters, myX, N, trial, 1)

plt.scatter(myX[:,0], myX[:,1])
plt.scatter(cluster_centers[:,0], cluster_centers[:,1],marker="X", c="red", s = 200)
plt.show()


# # 4 Training

# $fit\_cluster$ function takes $cluster\_centers$ and the data returns clusters for each points.

# In[9]:


def fit_cluster(cluster_centers, X, N, n_clusters):
   
    cluster = np.zeros(N)
    for j in range(N):
        clust_no = 0
        clust_dist = euclidian(cluster_centers[0], X[j])
        for i in range(1,n_clusters):
            cur_dist = euclidian(cluster_centers[i], X[j])
            if(clust_dist>cur_dist):
                clust_no = i
                clust_dist = cur_dist
        cluster[j] = clust_no

    return cluster 


# $train$ function repeats $fit\_cluster$ until convergence or max_iter. It returns final $cluster\_centers$ and converged $clusters$

# In[10]:


def train(cluster_centers, X, N, n_clusters, max_iter, verbose = True ):
    cluster = np.zeros(N)
    myIter = 0
    Continue_iter = True 
    p = X.shape[1]
    
    while (Continue_iter & (myIter<max_iter)):
        old_cluster = np.copy(cluster)
        cluster = fit_cluster(cluster_centers, X, N, n_clusters)

        if(np.mean(old_cluster == cluster) == 1):
            Continue_iter = False

        for i in range(n_clusters):
            cluster_centers[i,:] = np.mean(X[cluster == i], 0)

        myIter = myIter + 1
        
    if verbose:
        if (myIter<max_iter):
            print "algorithm has converged at iteration number", myIter
        else:
            print "algorithm did not converge"

        if p==2:
            
            mycolor = ["blue", "green", "orange", "firebrick", "grey"]
            
            for i in range(n_clusters):
                cond = (cluster == i)
                plt.scatter(X[cond,0], X[cond,1], marker='o', label=i, color=mycolor[i])
            plt.legend(numpoints=1, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            
            plt.show()

            
    return cluster, cluster_centers


# In[11]:


cluster, cluster_centers = train(cluster_centers, myX, N, n_clusters, max_iter, verbose = True )


# # 5 Prediction

# To prediction, we will generate 12 new points

# In[12]:


predMean = np.array([[0, 4], 
                     [3, 1],
                     [-5, 3],
                     [7, 4]])
n = 3
predX = generate_normal(n, predMean, 108)


# In[13]:


mycolors = ["blue", "green", "orange", "firebrick", "grey"]
for i in range(n_clusters):
    cond = (cluster == i)
    plt.scatter(myX[cond,0], myX[cond,1], marker='o', label=i, color = mycolors[i])
plt.legend(numpoints=1, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

plt.scatter(predX[:,0], predX[:,1],marker="X", c="black", s = 200)

plt.show()


# Here is prediction process, $fit\_cluster$ function also could be used as a prediction function K-means algorithm. 

# In[14]:


pred_clust = fit_cluster(cluster_centers, predX, predX.shape[0], n_clusters)


# In[15]:


mycolors = ["blue", "green", "orange", "firebrick", "grey"]

for i in range(n_clusters):
    cond = (cluster == i)
    plt.scatter(myX[cond,0], myX[cond,1], marker='o', label=i, color = mycolors[i])
    
plt.legend(numpoints=1, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    
for i in range(n_clusters):
    cond = (pred_clust == i)
    plt.scatter(predX[cond,0], predX[cond,1], marker='X', label=i, color = mycolors[i], s = 200)

plt.show()


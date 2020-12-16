# -*- coding: utf-8 -*-
"""
@author: Neha Bais

Script to find topics based on keywords of different titles.

-- LSA topic modelling algorithm 
-- UMAP dimensionality reduction to visualize the results

"""

import os
from extract_data import *
from helper_functions import *


# Extract data from PubMed
count_results, pub_data = extract_data()

# Remove duplicate titles
pub_data = pub_data.drop_duplicates(subset=['Title'], keep = 'first')  


# Data Pre-processing
clean_titles = [tokenize(title) for title in pub_data['Title']]   


# Create document term matrix
doc_term_matrix, vocab = create_bow(clean_titles)


##################################
#                                #
#        Topic Modeling          #
#  (Latent Semantic Analysis)    #
##################################

from sklearn.decomposition import LatentDirichletAllocation

# LDA for doc term amtrix 
LDA = LatentDirichletAllocation(n_components=6, random_state=42)
LDA.fit(doc_term_matrix)

print()

# Let's print the topics with 10 important words in them
for i,topic in enumerate(LDA.components_):
    print(f'Top 10 words for Topic-{i}:')
    print([vocab[i] for i in topic.argsort()[-10:]])
    print('\n')
   
    
# Topic-0: Obesity 
# Topic-1: Wearable
# Topic-2: Mental Health 
# Topic-3: Pandemic, Viral Infection
# Topic-4: Cancer
# Topic-5: Influenza    


# Let's assign the probability of all the topics to each document.
topic_values = LDA.transform(doc_term_matrix)
topic_values.shape   # (1949, 6)

# This shows that each document has 6 columns.
# Each column corresponds to probability value of a prticular topic.
# To find the topic index with maximum value, we will use argmax() and pass 1
# as the value for the axis parameter

# Let's add a new column for topic in dataframe and assigns topic value to each row
pub_data['Topic'] = topic_values.argmax(axis=1)
pub_data.to_csv('pub_data.csv', index=False)


###########################################
#                                         #    
#   Topic Visualization - Dendrogram      #
#                                         #
###########################################    

# For visualizing topic results, I am just taking a random sample of 
# around 50 articles and then plotting the clustering results on
# dendrogram.

number_of_rows = topic_values.shape[0]
random_indices = np.random.choice(number_of_rows, size=50, replace=False)

random_rows = topic_values[random_indices, :]
#random_rows.shape

from scipy.cluster.hierarchy import ward, dendrogram, linkage
import matplotlib.pyplot as plt
#from sklearn.metrics.pairwise import cosine_similarity

#linkage_matrix = ward(1-cosine_similarity(random_rows)) #define the linkage_matrix using ward clustering pre-computed distances
linkage_matrix = linkage(random_rows, 'ward')

fig, ax = plt.subplots(figsize=(25, 12)) # set size
ax = dendrogram(linkage_matrix, orientation='top', 
                labels = ['Article-'+ str(idx) for idx in random_indices],leaf_rotation=90., 
                leaf_font_size=15.);

plt.yticks(fontsize= 15) 
plt.title('Hierarchical Clustering Dendrogram\n',  fontsize=35)
plt.ylabel('Distance',  fontsize=25)
plt.tight_layout() #show plot with tight layout

plt.show()

# Topic-0: Obesity -- Purple
# Topic-1: Wearable -- Green
# Topic-2: Mental health -- Black
# Topic-3: Pandemic -- Blue
# Topic-4: Cancer  - Yellow
# Topic-5: Influenza -- Red


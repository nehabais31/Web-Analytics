# -*- coding: utf-8 -*-
"""
@author: Neha Bais
MET CS-688 Fall'20

Script to visualize data
1. Overall Freq of keywords
2. Area plot for visualising freq of keywords over diff years.
3. Density plot to see the distribution of keywords over years.

"""


#import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from extract_data import *


# Extract data from Pubmed
count_results, pub_data = extract_data()

# Get overall count of each keyword
keyword_count = count_results.sum(axis=1).to_dict()
keyword_count = {k: v for k, v in sorted(keyword_count.items(), 
                                         key=lambda item: item[1], reverse=True)}


#################################################
#                                               #
#  Plotting overall frequency for each keyword  #
#                                               #
#################################################
plt.figure(figsize = (5,5))
plt.bar(list(keyword_count.keys()), keyword_count.values(), color='royalblue')
plt.title('Keyword frequency from article titles')  
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.xticks(rotation = 45)
plt.show()

    
####################
#                  #
#     Area Plot    #
#                  #
####################    
    
plt.figure(figsize = (20,10))
count_results.T.plot.area()
plt.title('Area plot for all Keyword Frequencies', fontsize=15)
plt.xlabel('Years')
plt.xticks(count_results.T.index)
plt.ylabel('Frequencies')
plt.legend(loc=2,
           bbox_to_anchor=(1.05, 1.0), 
           borderaxespad=0.)
plt.show() 


####################################################
#                                                  #
# Distribution of keywords articles over 9 years   #
#           (Density Plot)                         #
####################################################  

# Get year counts in a list for each keyword in order to plot them
x = {}
for keyword in count_results.index:
    val_count = []
    for idx, year in enumerate(count_results.loc[keyword].index):
        count = np.repeat(year,count_results.loc[keyword].values[idx]).flatten()
        val_count.extend(count)
        x[keyword] = val_count

        
# Since Covid data articles are highly right skewed, not visualising covid-19  
x.pop('Covid-19', None)
for word in x.keys():
    sns.distplot(x[word], kde=True, hist = True)
    plt.xlabel('Year')
    plt.ylabel('Density')
    plt.title('Density plot for ' + word)
    plt.show()
        


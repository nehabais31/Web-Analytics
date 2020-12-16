# -*- coding: utf-8 -*-
"""
@author: Neha Bais
MET CS-688 Fall'20

Script to perform statistical test on data
fetched from Pubmed.

1. Visualising distribution of data for each keyword.
2. Performed statistical test based on distribution.

Non-Parametric -- Kruskal Wallis 
                  Mann Whitney U test

"""

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from extract_data import *


# Extract data from Pubmed
count_results, pub_data = extract_data()

# Write data to csv file
count_results.to_csv('count_results.csv')
pub_data.to_csv('pub_data.csv', index=False)



###################################
#                                 # 
#     Non-Parametric Test         #
#  (Distribution not normal)      #
#                                 #
###################################

# Kruskal Wallis Test
# H0: All sample distributions are equal
# H1: Atleast 2 samples have different distribution

obesity     = count_results.loc['Obesity'].values    
cancer      = count_results.loc['Cancer'].values 
covid       = count_results.loc['Covid-19'].values
wearable    = count_results.loc['Wearable'].values
mental_hlth = count_results.loc['Mental Health'].values
influenza   = count_results.loc['Influenza'].values

kw_stat, kw_p = stats.kruskal(obesity, cancer, covid,  wearable, mental_hlth, influenza)

print('\n\tKruskal Wallis test results' )
print('\t=============================\n')
print(f'KW test p-value: {kw_p}')
print('There is a significant difference between atleast 2 groups' \
      if kw_p < 0.05 else 'There is no significant difference between all groups')

# p-value = 1.8734213393064586e-08 which is less than 0.05
# We can reject the Null hypothesis and can say that there is a significant
# difference between atleasts 2 groups(keywords frequencies over years).

# To find out which two groups(keywords) are significantly different, we will
# perform Mann-Whitney U test.

# Mann-Whitney U Test

stats_data = [obesity, cancer, covid, wearable, mental_hlth, influenza]

print('\n\tMann-Whitney group wise stats results: ')
print('\t=======================================')

kw_1 = []
kw_2 = []
p_value = []
for i in range(len(stats_data)-1):
    for j in range(i+1, len(stats_data)-1):
        _ , mwu_p = stats.mannwhitneyu(stats_data[i], stats_data[j], 
                                   alternative = 'two-sided') 
    
        #print(f'{count_results.index[i]} - {count_results.index[j]} \n p-value: {mwu_p}\n')
        kw_1.append(count_results.index[i])
        kw_2.append(count_results.index[j])
        p_value.append(mwu_p)
 
stats_results = {'Keyword-1': kw_1, 'Keyword-2': kw_2, 'p-value': p_value}     
mwu_df = pd.DataFrame(stats_results)   
print(mwu_df)     
        
# Conclusion --
# Except Obesity and Mental Health (p-value = 0.25), all other groups have significant  p-values.
# For all other keyword pairs p-value is less than 0.05.        

       
#data = data.drop_duplicates(subset=['Title'], keep = 'first')        
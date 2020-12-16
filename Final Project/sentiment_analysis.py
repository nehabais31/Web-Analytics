# -*- coding: utf-8 -*-
"""
@author: Neha Bais
MET CS-688 Fall'20

Script to perform sentiment analysis
on titles of articles fetched from PubMed.

"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from afinn import Afinn
from extract_data import *
from helper_functions import *


# Fetch data from Pubmed
count_results, pub_data = extract_data()

# Remove duplicate titles
pub_data = pub_data.drop_duplicates(subset=['Title'], keep = 'first')  


# Data Pre-processing
clean_titles = [tokenize(title) for title in pub_data['Title']]   

# Calculate sentiment for each title
afinn = Afinn()
afinn_score = [afinn.score(title) for title in clean_titles]

# Add afinn score column to our dataframe
pub_data = pub_data.assign(Afinn_Score = afinn_score)

# Let's see the overall sentiment for each keyword
print('Overall sentiment score for each keyword:')
print('==========================================')
print(pub_data.groupby('Keyword').agg({'Afinn_Score' : sum}).reset_index())

# Except Wearable articles, all other keyword titles got a negative score

# Now, let's find out the sentiment for eack keyword articles year wise
afinn_year = pub_data.groupby(['Keyword', 'Year']).agg({'Afinn_Score' : sum}).\
                reset_index()
   
afinn_year = afinn_year.append({'Keyword':'Cancer', 'Year': 2012 ,
                                'Afinn_Score': -10.0}, ignore_index = True) 
afinn_year = afinn_year.append({'Keyword':'Covid-19', 'Year': 2012 ,
                                'Afinn_Score': -0.0}, ignore_index = True)   
                
afinn_year = afinn_year.sort_values(by=['Keyword', 'Year'])
afinn_year = afinn_year.reset_index(drop=True)
print('\n\nSentiment score for each keyword year wise')
print('===========================================')
print(afinn_year)


# Visualising sentiment trajectory over years for each eyword
keywords = ['Obesity', 'Cancer', 'Covid-19', 'Wearable', 'Mental Health', 'Influenza'] 

year = [2012,2013,2014,2015,2016,2017,2018,2019,2020]

for keyword in keywords:
    #year = afinn_year[afinn_year['Keyword'] == keyword]['Year'].unique()
    sentiment = afinn_year[afinn_year['Keyword'] == keyword]['Afinn_Score']
    
    # Plot these results
    plt.plot(year, sentiment, label = keyword, marker='o', markersize = 4)
    plt.xlabel('Year')
    plt.ylabel('Sentiment Score')
    plt.title('Sentiment trajectory over years')
plt.legend(loc=2,
           bbox_to_anchor=(1.05, 1.0), 
           borderaxespad=0.)  
plt.show()
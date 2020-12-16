"""
@author: Neha Bais
MET CS-688 Fall'20

Script to fetch data from Pubmed for Years: 2012 to 2020 

Keywords: 'Obesity'       
         'Cancer'          
         'Covid-19'        
         'Wearable'        
         'Mental Health'   
         'Influenza'       
                                      
"""

from Bio import Entrez
import pandas as pd
import re
import numpy as np
import time
import matplotlib.pyplot as plt



def fetch_article_data(id_list):
    ids = ','.join(id_list)
    
    Entrez.email = 'nehabais31@gmaill.com'
    handle = Entrez.efetch(db = 'pubmed',
                           retmode = 'xml',
                           id = ids)
    
    records = Entrez.read(handle)
    article_data = records['PubmedArticle']
    
    return article_data    
    

def search_data(keyword, year):
    Entrez.email = 'nehabais31@gmaill.com'
    handle = Entrez.esearch(db = 'pubmed',
                            sort = 'relevant',
                            retmode = 'xml',
                            retmax = 50,
                            term = ' '.join([keyword, str(year)+'[pdat]']))
    
    record = Entrez.read(handle)
    rec_count = record['Count']
    id_list =  record['IdList']
    
    return rec_count, id_list


def extract_data():
    keywords = ['Obesity', 'Cancer', 'Covid-19', 'Wearable', 'Mental Health', 'Influenza']    
    years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

    # Initializing dataframe for capturing record count each month
    # And storing titles for each keyword for each year
    count_results = pd.DataFrame(index=keywords, columns = years)
    pub_data = pd.DataFrame()


    start_time = time.time()
    print('Processing...')

    for k in keywords :
        for y in years:
            # Get ids and count for articles
            rec_count, id_list = search_data(k, y)
            count_results.loc[k,y] = rec_count
        
            # Fetch article data using ids
            pubmed_article = fetch_article_data(id_list)
        
            title = []
        
            # Extract titles only from the overall data
            for article in pubmed_article :
                article_title = article['MedlineCitation']['Article']['ArticleTitle']
                title.append(article_title)    
            
                # Create a dataframe for each keyword results
                article_df = pd.DataFrame({'Keyword': k, 'Year': y, 'Title' : title})
       
            # Final dataframe for titles of both keywords
            pub_data = pd.concat([pub_data, article_df]) 
       
    count_results = count_results.applymap(eval)
    
    print('Data extraction completed !!!')
    print(f'Time taken for fetching data: {round(time.time() - start_time, 4)} sec.')
    
    
    return count_results, pub_data
       
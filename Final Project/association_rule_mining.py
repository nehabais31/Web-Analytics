# -*- coding: utf-8 -*-
"""
@author: Neha Bais
MET CS-688 Fall'20

Script to find the frequent occuring words 
in titles of Pubmed Articles for each year.

"""

#pip install mlxtend

import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from extract_data import *
from helper_functions import *


def association_rule(years, min_supp, min_confidence):
    '''
    This function will calculate the frequent words 
    based on the articles of different years.
    ===============================================
    Input: list of years
    Output: Resulting rules dataframe

    '''
    rules_df = pd.DataFrame()
    
    for year in years:
        freq_itemsets = apriori(dtm_df[dtm_df.index == year], 
                                min_support=min_supp, verbose = 1,
                                use_colnames=True)
    
        # Create the rules
        rules = association_rules(freq_itemsets, 
                          metric="lift")
        
        rules['Year'] = year 
        rules = rules[['Year','antecedents', 'consequents',
                       'support', 'confidence', 'lift']]

        rules = rules[rules['confidence'] >= min_confidence]
    
        rules_df = pd.concat([rules_df, rules]).reset_index(drop=True)
    
    return rules_df


if __name__ == '__main__' :
    
    # Extract data from PubMed
    count_results, pub_data = extract_data()

    # Remove duplicate titles
    pub_data = pub_data.drop_duplicates(subset=['Title'], keep = 'first')  


    # Data Pre-processing
    clean_titles = [tokenize(title) for title in pub_data['Title']]  

    # Create Document term matrix
    title_dtm, vocab = create_bow(clean_titles)

    # Sort the word dictionary
    #words = [k for k, v in sorted(vocab, key=lambda item: item[1])]
    words = sorted(vocab)

    # Create a dataframe from Bag of words results
    dtm_df = pd.DataFrame(title_dtm.toarray(), columns = words, 
                      index = pub_data['Year'].tolist())

    # Encoding words data, 
    #if present more than 0 times assign 1 else 0
    dtm_df = dtm_df.applymap(lambda x: 0 if x <= 0 else 1)

    # Get unique years list and feed to apriori algorithm
    years = pub_data['Year'].unique()
    
    rules_df = association_rule(years, min_supp = 0.03, min_confidence = 0.7)

    print('\n\n\t\tFrequent itemsets for each year')
    print('==================================================================')
    print(rules_df)
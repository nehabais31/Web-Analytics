# -*- coding: utf-8 -*-
"""
@author: Neha Bais

Script containing some helper functions used by multiple scripts
1. Tokenizing and stemming
2. Creating bag of words
3. Creating TF-IDF matrix

"""

import numpy as np
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer


def tokenize(sentence):
    '''
    This function will tokenize and stem each article titles.
    =========================================================
    Input: Each article title
    Returns: Tokenized title with 
             a. No Punctuations
             b. No Stop words
             c. Words converted to their root form
    '''
    lemma = WordNetLemmatizer() 
    p_stemmer = PorterStemmer()
    
    # Keeping only alphabets and numbers and removing special chars.
    clean_titles = " ".join(re.sub("([^A-Za-z \t])", ' ', sentence).split()) 
        
    # Tokenizing and removing stop words
    stop_free = ' '.join([word for word in clean_titles.lower().split() \
                          if word not in stopwords.words('english') and 
                          len(word) > 3])
    
    # Normalizing words to their root form
    normalized = ' '.join([lemma.lemmatize(word, pos='v') 
                           for word in stop_free.split()]) 
        
    return normalized


def create_bow(clean_titles):
    '''
    This function will create a bag of words for the article titles
    ================================================================
    Input:   Article titles
    Returns: bag of words containing only 100 most freq words 
    '''
       
    from sklearn.feature_extraction.text import CountVectorizer

    vectorizer = CountVectorizer(max_df=0.8, min_df=2)
    doc_term_matrix = vectorizer.fit_transform(clean_titles)
    
    return doc_term_matrix, vectorizer.get_feature_names() #vectorizer.vocabulary_ 


def create_tfidf(clean_titles):
    '''
    This function will create a document term matrix for the article titles
    =======================================================================
    Input:   Bag of words created
    Returns: DTM matrix with 100 most freq words
    '''
    
    # Create Document term matrix 
    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorizer = TfidfVectorizer(smooth_idf=True)
    tfidf = vectorizer.fit_transform(clean_titles)
    
    return tfidf.toarray(), vectorizer.get_feature_names()

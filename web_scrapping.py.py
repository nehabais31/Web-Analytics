# -*- coding: utf-8 -*-
"""
Neha Bais
MET CS-688 

1. Scrap pubmed website and collect 50 
   articles' titles and abstracts including the keyword COVID-19.
2. Create a histogram of drequency f mentioned words.

"""

import requests
from bs4 import BeautifulSoup
import csv
import numpy as np
import re
import itertools
import collections
import matplotlib.pyplot as plt


def plot_figure(my_words_count):
    plt.bar(list(my_words_count.keys()), my_words_count.values(), color='g')
    plt.title('Word frequency from article titles')  
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation = 45)
    plt.show()
    

def rm_spcl_char(title) :
    '''
    Cleaning text of all the titles 
    Keeping only alphabets and numbers and removing special chars.
    '''
    return " ".join(re.sub("([^0-9A-Za-z \t])", '', title).split())


def get_word_freq(title_list) :
    '''
    Get the frequency of words in the article's titles
    '''
    title_lst_clean = [rm_spcl_char(titles) for titles in title_list]    
    print(title_lst_clean)
    words_in_title = [title.lower().split() for title in title_lst_clean]

    # flatten all words in a single list
    all_words = list(itertools.chain(*words_in_title))

    # Create counter
    count_words = collections.Counter(all_words)

    # Get the count of desired words
    my_words = ['review', 'diagnosis', 'treatment', 'clinical']
    my_words_count = {}

    for word in my_words:
        if word in count_words :
            my_words_count[word] = count_words[word]
    
    my_words_count =  {k : v for k, v in sorted(my_words_count.items(), 
                        key = lambda item: item[1], reverse = True)} 
    
    return  my_words_count   
    

def scrape_article_abstract(article_link) :
    '''
    Get the abstract of each article by
    scraping each article page
    '''
    article_page = requests.get(article_link)
    article_soup = BeautifulSoup(article_page.text, 'html.parser')
    
    abstract = article_soup.find('div', class_ = 'abstract-content selected').text
    return abstract.strip()


if __name__  == '__main__' :
    csv_file = open('article_scrape.csv', 'w', encoding="utf-8")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Title', 'Abstract', 'Artile link'])
    
    
    base_url = 'https://www.ncbi.nlm.nih.gov/pubmed'
    search_kw = '/?term=covid-19'

    # scrap data from 5 pages as each page contains 10 articles    
    pages = np.arange(1,6)

    # list for storing each article title
    title_list = []

    for page in pages :
        source = requests.get(base_url + search_kw + f'&page={page}')
        soup = BeautifulSoup(source.text, 'html.parser')

        # select the entire desired section of entire page
        results = soup.find('div', class_ = 'search-results-chunk results-chunk')

        # Get all articles
        articles = results.find_all('div', class_ = 'docsum-content')

        for article in articles :
            try:
                title = article.a.text
                article_id = article.a.get('href')
                article_link = base_url + article_id
                article_abst = scrape_article_abstract(article_link)
                title_list.append(title.strip())
            
                print('Title: ', title.strip())
                #print('Abstract: ', article_abst)
            except Exception as e:
                pass
    
            # write data to a csv file
            csv_writer.writerow([title.strip(), article_abst, article_link])
    
    csv_file.close()  

    # Counting frequency of words in articles title
    my_words_count = get_word_freq(title_list)

    # Plot histogram of word frequency
    plot_figure(my_words_count)  
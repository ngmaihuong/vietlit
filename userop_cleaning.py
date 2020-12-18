#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author:         Sierra Nguyen
Date created:   12/08/2020
Date updated:   12/18/2020
Title:          VietLit User Survey Data Cleaning
"""

# change working directory
import os
os.chdir('/Users/Boo Boo/Downloads/VietLit')

# importing modules
import pandas as pd
import string
from collections import Counter

# enabling displaying all columns
pd.set_option('display.max_columns', None)

# importing data
df = pd.read_excel('userdata.xlsx')

# removing redundant column
df1 = df.drop(columns=[df.iloc[: , 3].name])

# question for human processing
interest = df1.iloc[:, 2]

# criteria column
crit = df1.iloc[:, 0]

# reason column
reas = df1.iloc[:, 1]

# processing responses

def prepro(df):
    master_string = ''
    
    #combining all cells into a paragraph
    for i in range(len(df)):
        master_string += df.iloc[i]
        
    #stripping punctuations
    master_string = master_string.translate(str.maketrans('', '', string.punctuation))
    
    #splitting master string into a list of words
    master_list = master_string.split()
    master_list = [x.lower() for x in master_list]
    
    #getting list of words and counts
    word_count = dict(Counter(master_list))

    word_count = pd.DataFrame.from_dict(word_count, orient='index')
    word_count = word_count.rename(columns={0: 'ct'})
    
    #filtering by count
    word_count = word_count[word_count.ct > 5]
    
    return word_count

crit_count = prepro(crit)
reas_count = prepro(reas)

# playing around with newly found Vietnamese NLP toolkit

#pip install underthesea

master_string = ''

# combining all cells into a paragraph
for i in range(df1.shape[1]):
    for j in range(df1.shape[0]):
        master_string += ' ' + df1.iloc[j, i]

# stripping punctuation
master_string = master_string.translate(str.maketrans('', '', string.punctuation)).lower()

# importing underthesea NLP
from underthesea import word_tokenize

# word segmentation
tokenized_master_string = word_tokenize(master_string)

# getting list of words and counts
word_count = dict(Counter(tokenized_master_string))

word_count = pd.DataFrame.from_dict(word_count, orient='index')
word_count = word_count.rename(columns={0: 'ct'})

# filtering by count
word_count = word_count[word_count.ct > 5]

# POS tagging
    
# =============================================================================
#     A - Adjective
#     C - Coordinating conjunction
#     E - Preposition
#     I - Interjection
#     L - Determiner
#     M - Numeral
#     N - Common noun
#     Nc - Noun Classifier
#     Ny - Noun abbreviation
#     Np - Proper noun
#     Nu - Unit noun
#     P - Pronoun
#     R - Adverb
#     S - Subordinating conjunction
#     T - Auxiliary, modal words
#     V - Verb
#     X - Unknown
#     F - Filtered out (punctuation)
# =============================================================================
    
from underthesea import pos_tag

word_tag = list(word_count.index.values)
for i in range(len(word_count)):
    word_tag[i] = pos_tag(word_count.index[i])[0]

# finding a list of POS
key_list = list(word_count.index.values)
values_list = []

for i in range(len(word_tag)):
    values_list.append(word_tag[i][1])

word_tag_dict = dict(zip(key_list, values_list))
pos_list = set(list(word_tag_dict.values()))

# getting list of relevant words   
word_cloud = []
for item in word_tag:
    if item[1] in ['A', 'M', 'N', 'V']:
        if (len(item[0]) in [2, 3]) and item[1] == 'A':
            word_cloud.append(item[0])
        elif (len(item[0]) in [4, 5] and item[1] in ['A', 'M']):
            word_cloud.append(item[0])
        elif len(item[0]) > 5:
            word_cloud.append(item[0])

# retaining count of relevant words
word_count = word_count.reset_index()
word_cloud = pd.DataFrame(word_cloud, columns=['word'])
word_cloud = pd.merge(word_cloud, word_count, how='left', right_on='index', left_on='word').drop(columns=['index']).dropna()

# exporting
interest.to_excel('vietlist_user_interest.xlsx', index = True)
word_cloud.to_excel('vietlit_word_cloud.xlsx', index = True)

# end


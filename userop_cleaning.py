#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author:         Sierra Nguyen
Date created:   12/08/2020
Date updated:   12/17/2020
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

# =============================================================================
# # POS tagging
# from underthesea import pos_tag
# tagged_master_string = pos_tag(master_string)
# 
# # sentiment analysis
# from underthesea import sentiment
# for i in range(len(interest)):
#     interest[i] = sentiment(interest[i])
# =============================================================================

# =============================================================================
# # separating the data set into long and short responses
# long_answer_row = []
# short_answer_row = []
# 
# for i in range(len(crit)):
#     if len(crit[i]) > 75:
#         long_answer_row.append(i)
#     else:
#         short_answer_row.append(i)
# 
# crit_long = crit.iloc[long_answer_row]
# crit_short = crit.iloc[short_answer_row]
#         
# for i in range(len(reas)):
#     if len(reas[i]) > 75:
#         long_answer_row.append(i)
#     else:
#         short_answer_row.append(i)
# 
# reas_long = reas.iloc[long_answer_row]
# reas_short = reas.iloc[short_answer_row]
# 
# # =============================================================================
# # for i in range(df1.shape[0]):
# #     for j in range(df1.shape[1]):
# #         if len(df1.iloc[i, j]) > 100:
# #             long_answer_row.append(i)
# #         else:
# #             short_answer_row.append(i)
# # =============================================================================
# 
# def get_unique(index_list):
#     index_list = set(index_list)
#     index_list = list(index_list)
#     return index_list
#     
# long_answer_row = get_unique(long_answer_row)
# short_answer_row = get_unique(short_answer_row)
# 
# df2 = df1.iloc[long_answer_row]
# df3 = df1.iloc[short_answer_row]
# 
# # exporting tables
# df2.to_excel('long_resp.xlsx', index = True)
# df3.to_excel('short_resp.xlsx', index = True)
# 
# master_string = ''
# 
# # processing short responses
# 
# # combining all cells into a paragraph
# for i in range(df3.shape[1]):
#     for j in range(df3.shape[0]):
#         master_string += ' ' + df3.iloc[j, i]
# 
# # stripping punctuation
# master_string = master_string.translate(str.maketrans('', '', string.punctuation))
# 
# # splitting master string into a list of words       
# master_list = master_string.split()
# master_list = [x.lower() for x in master_list]
# 
# # getting list of words and counts
# word_count = dict(Counter(master_list))
# 
# word_count = pd.DataFrame.from_dict(word_count, orient='index')
# word_count = word_count.rename(columns={0: 'ct'})
# 
# # filtering by count
# word_count = word_count[word_count.ct > 4]
# 
# # filtering by word
# drop_list = [' người ', ' đọc ', ' truyện ', ' và ', ' cần ', ' sẽ ', ' mình ', ' đủ ', ' quá ', 
#              ' là ', ' được ', ' ạ ', ' vì ', ' chưa ', ' nên ', ' sách ', ' với ', ' việt ', ' văn ', 
#              ' để ', ' cũng ', ' như ', ' k ', ' từ ', ' nơi ', ' cho ', ' hơn ', ' muốn ', ' mọi ', ' rất ', 
#              ' thì ', ' ở ', ' khá ', ' nó ', ' vậy ', ' mong ']
# drop_list_no_space = [x.strip(' ') for x in drop_list]
# word_count = word_count.drop(drop_list_no_space)#.reset_index().rename(columns={'index': 'word'})
# 
# # stripping punctuations and words with no meanin
# for i in range(df2.shape[1]):
#     for j in range(df2.shape[0]):
#        df2.iloc[j, i] = df2.iloc[j, i].translate(str.maketrans('', '', string.punctuation))
#        for k in range(len(drop_list)):
#            if drop_list[k] in df2.iloc[j, i]:
#                df2.iloc[j, i] = df2.iloc[j, i].replace(drop_list[k], ' ')
# =============================================================================
       
# =============================================================================
# # exporting list for Tableau
# from pandas import DataFrame
# wc_df = DataFrame(master_list)
# wc_df.to_excel('short_resp_wc.xlsx', index=True)
# =============================================================================


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author:         Sierra Nguyen
Date created:   12/08/2020
Date updated:   12/12/2020
Title:          VietLit User Survey Data Cleaning
"""

# change working directory
import os
os.chdir('/Users/Boo Boo/Downloads/VietLit')

# importing modules
import pandas as pd
import numpy as np

# enabling displaying all columns
pd.set_option('display.max_columns', None)

# importing data
df = pd.read_excel('userdata.xlsx')

# removing redundant column
df1 = df.drop(columns=[df.iloc[: , 3].name])

# separating the data set into long and short responses
long_answer_row = []
short_answer_row = []

for i in range(df1.shape[0]):
    for j in range(df1.shape[1]):
        if len(df1.iloc[i, j]) > 65:
            long_answer_row.append(i)
        else:
            short_answer_row.append(i)
  
def get_unique(index_list):
    index_list = set(index_list)
    index_list = list(index_list)
    return index_list
    
long_answer_row = get_unique(long_answer_row)
short_answer_row = get_unique(short_answer_row)

df2 = df1.drop(long_answer_row)
df3 = df1.drop(short_answer_row)

# exporting tables
df2.to_excel('short_resp.xlsx', index = True)
df3.to_excel('long_resp.xlsx', index = True)

master_string = ''

# processing short responses

# combining all cells into a paragraph
for i in range(df2.shape[1]):
    for j in range(df2.shape[0]):
        master_string += ' ' + df2.iloc[j, i]

# stripping punctuation
import string
master_string = master_string.translate(str.maketrans('', '', string.punctuation))

# splitting master string into a list of words       
master_list = master_string.split()
master_list = [x.lower() for x in master_list]

# getting list of words and counts
from collections import Counter
word_count = dict(Counter(master_list))

word_count = pd.DataFrame.from_dict(word_count, orient='index')
word_count = word_count.rename(columns={0: 'ct'})

# filtering by count
word_count = word_count[word_count.ct > 4]

# filtering by word
drop_list = ['người', 'đọc', 'truyện', 'và', 'cần', 'sẽ', 'mình', 'đủ', 'quá', 'là', 'được', 'ạ', 'vì', 'chưa', 'nên', 'sách', 'với', 'việt',  'văn', 'để', 'cũng', 'như', 'k', 'từ', 'nơi', 'cho', 'hơn', 'muốn', 'mọi', 'rất', 'thì', 'ở', 'khá', 'nó', 'vậy', 'mong']
word_count = word_count.drop(drop_list).reset_index().rename(columns={'index': 'word'})

# exporting list for Tableau
from pandas import DataFrame
wc_df = DataFrame(master_list)
wc_df.to_excel('short_resp_wc.xlsx', index=True)


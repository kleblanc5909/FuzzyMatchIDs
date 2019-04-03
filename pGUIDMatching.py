# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 14:02:03 2019

@author: Kim LeBlanc
"""

import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def match_two_collections(smallList,masterList,theLimit):
    results=[]
    for member in smallList:
        x=process.extract(member, masterList, limit=theLimit)
        results.append(x)
    return results

df = pd.read_csv("pGUID_Matching.csv", engine='python')

blackList=['NDAR_INV']
for pattern in blackList:
    df['AllRutgers'] = df['AllRutgers'].str.replace(pattern, '')

#datasets
Unique_DAIC_IDs = df['UniqueDAIC'].dropna()
Unique_Rutgers_IDs = df['UniqueRutgers'].dropna()
AllRutgersIDs = df['AllRutgers'].dropna()
AllDAIC_IDs = df['AllDAIC']

resultLimit=2
 
BestMatches_DtoR = match_two_collections(Unique_DAIC_IDs,AllRutgersIDs, resultLimit)
BestMatches_RtoD = match_two_collections(Unique_Rutgers_IDs, AllDAIC_IDs, resultLimit)
 
df['BestMatchesdf_DtoR']=pd.Series(BestMatches_DtoR)
df['BestMatchesdf_RtoD']=pd.Series(BestMatches_RtoD)
 
df.to_csv("FuzzyMatchedIDs.csv")

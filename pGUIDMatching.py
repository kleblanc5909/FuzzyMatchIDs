# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 14:02:03 2019

@author: Kim LeBlanc
"""

import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def match2Lists(list1,list2,theLimit):
    """
    Loops over a list and returns fuzzy matches found in a second list.
    Inputs:
      list1 - list of terms to search for in the master list
      list2 - master list that is searched for matches over and over
      theLimit - number of fuzzy match results to return
    """
    results=[]
    for member in list1:
        x=process.extract(member, list2, limit=theLimit)
        results.append(x)
    return results

df = pd.read_csv("pGUID_Matching.csv", engine='python')
print ('Finished reading in input file.')

blackList=['NDAR_INV']
for pattern in blackList:
    df['AllRutgers'] = df['AllRutgers'].replace(pattern, '')
    
#datasets
Unique_DAIC_IDs = df['UniqueDAIC'].dropna()
Unique_Rutgers_IDs = df['UniqueRutgers'].dropna()
AllRutgersIDs = df['AllRutgers'].dropna()
AllDAIC_IDs = df['AllDAIC']

resultLimit=2

print ('About to start first match2collections.') 
BestMatches_DtoR = match2Lists(Unique_DAIC_IDs,AllRutgersIDs, resultLimit)
print ('Just finished first match2collections.') 
print ('About to start second match2collections.') 
BestMatches_RtoD = match2Lists(Unique_Rutgers_IDs, AllDAIC_IDs, resultLimit)
print ('Just finished second match2collections.') 
 
df['BestMatchesdf_DtoR']=pd.Series(BestMatches_DtoR)
df['BestMatchesdf_RtoD']=pd.Series(BestMatches_RtoD)
 
df.to_csv("FuzzyMatchedIDs.csv")

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 14:02:03 2019

@author: Kim LeBlanc
"""

import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

BestMatches_DtoR_array=[]
BestMatches_RtoD_array=[]

def match_names_DtoR(DAIC_IDs,All_Rutgers_IDs,theLimit):
    for GUID in DAIC_IDs:
        x=process.extract(GUID, All_Rutgers_IDs, limit=theLimit)
        BestMatches_DtoR_array.append(x)
    return BestMatches_DtoR_array

def match_names_RtoD(Rutgers_IDs,All_DAIC_IDs,theLimit):
    for GUID in Rutgers_IDs:
        x=process.extract(GUID, All_DAIC_IDs, limit=theLimit)
        BestMatches_RtoD_array.append(x)
    return BestMatches_RtoD_array
 
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
 
BestMatches_DtoR = match_names_DtoR(Unique_DAIC_IDs,AllRutgersIDs, resultLimit)
BestMatches_RtoD = match_names_RtoD(Unique_Rutgers_IDs, AllDAIC_IDs, resultLimit)
 
df['BestMatchesdf_DtoR']=pd.Series(BestMatches_DtoR)
df['BestMatchesdf_RtoD']=pd.Series(BestMatches_RtoD)
 
df.to_csv("FuzzyMatchedIDs.csv")

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

def match_names_DtoR(DAIC_IDs,All_Rutgers_IDs):
    for GUID in DAIC_IDs:
        x=process.extract(GUID, All_Rutgers_IDs)
        BestMatches_DtoR_array.append(x)
    return BestMatches_DtoR_array

def match_names_RtoD(Rutgers_IDs,All_DAIC_IDs):
    for GUID in Rutgers_IDs:
        x=process.extract(GUID, All_DAIC_IDs)
        BestMatches_RtoD_array.append(x)
    return BestMatches_RtoD_array
 
df = pd.read_csv("pGUID_Matching.csv", engine='python')

#datasets

Unique_DAIC_IDs = df['UniqueDAIC'].dropna()
Unique_Rutgers_IDs = df['UniqueRutgers'].dropna()
AllRutgersIDs = df['AllRutgers'].dropna()
AllDAIC_IDs = df['AllDAIC']
 
BestMatches_DtoR = match_names_DtoR(Unique_DAIC_IDs,AllRutgersIDs)
BestMatches_RtoD = match_names_RtoD(Unique_Rutgers_IDs, AllDAIC_IDs)
 
df['BestMatchesdf_DtoR']=pd.Series(BestMatches_DtoR)
df['BestMatchesdf_RtoD']=pd.Series(BestMatches_RtoD)
 
df.to_csv("FuzzyMatchedIDs.csv")



#NumResults = 4
#finalResults1 = []
#for i in range(NumResults):
#    finalResults1.append([])

#turn series from df into list 1  (short list)
#turn series from df into parent list

#design a loop over each value in list 1
#for misPattern in listOne:
    #   perform fuzzy check on each list 1 item
#    tupleList = process.extract(misPattern, parentList1, limit=NumResults)
#    
#    for i in range(NumResults):
#        finalResults[i].append(tupleLIst[i][1])

#convert finalResults1 into 4 pd.Series
#build new pd.DF1  that is list 1 as series + new 4 pd.Series

#write out new pd.DF1

#repeat ALLL for other short list (list 2) and its parent list

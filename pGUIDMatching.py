# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 14:02:03 2019

@author: Kim LeBlanc
"""

import pandas as pd
from pandas import ExcelWriter
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def match2Lists(list1,list2):
    """
    Loops over a list and returns fuzzy matches found in a second list.
    Inputs:
      list1 - list of terms to search for in the master list
      list2 - master list that is searched for matches over and over
    """
    TopMatch = []
    TopScore = []
    TopRowIdx = []
    for member in list1:
        x=process.extractOne(member, list2)
        TopMatch.append(x[0])
        TopScore.append(x[1])
        TopRowIdx.append(x[2])
    return TopMatch, TopScore, TopRowIdx

df = pd.read_excel("ABCD_MasterList_pGUIDs_RUIDs.xlsx")
print ('Finished reading in input file.')

blackList=['NDAR_INV']
for pattern in blackList:
    df['pGUID_Rutgers'] = df['pGUID_Rutgers'].replace(pattern, '')
    
#datasets
Unique_DAIC_IDs = df['UniqueDAIC'].dropna()
Unique_Rutgers_IDs = df['UniqueRutgers'].dropna()
AllRutgersIDs = df['pGUID_Rutgers'].dropna()
AllDAIC_IDs = df['pGUID_DAIC']



print ('About to start first match2collections.') 
BestMatch_DtoR, BestScore_DtoR, BestRowIdx_DtoR = match2Lists(Unique_DAIC_IDs,AllRutgersIDs)
print ('Just finished first match2collections.') 
print ('About to start second match2collections.') 
BestMatch_RtoD, BestScore_RtoD, BestRowIdx_RtoD = match2Lists(Unique_Rutgers_IDs, AllDAIC_IDs)
print ('Just finished second match2collections.') 
 
df['BestMatchdf_DtoR']=pd.Series(BestMatch_DtoR)
df['BestScoredf_DtoR']=pd.Series(BestScore_DtoR)
df['BestMatchdf_RtoD']=pd.Series(BestMatch_RtoD)
df['BestScoredf_RtoD']=pd.Series(BestScore_RtoD)
df['BestRowIdxdf_DtoR']=pd.Series(BestRowIdx_DtoR)
df['BestRowIdxdf_RtoD']=pd.Series(BestRowIdx_RtoD)

RUID_DtoR_List = []
for rowIdx in BestRowIdx_DtoR:
    #workingRUID=df['RUID_Rutgers'].toList()[rowIdx]
    workingRUID=df['RUID_Rutgers'].iloc[rowIdx]
    RUID_DtoR_List.append(workingRUID)

df['RUID_DtoR']=pd.Series(RUID_DtoR_List)
 
writer = pd.ExcelWriter('FuzzyMatchedIDsOne.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()

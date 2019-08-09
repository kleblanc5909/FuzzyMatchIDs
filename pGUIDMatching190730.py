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

def createRUID_List(rowIdxList, headerStr):
    """
    Loops over a series containing row indices and returns a list of RUID strings.
    Inputs:
      rowIdxList - collection of row index values 
      headerStr - DataFrame header string value for column containing RUIDs
    Outputs:
      new list containing RUID strings
    """
    RUID_List = []
    for aRowIdx in rowIdxList:
        workingRUID=df[headerStr].iloc[aRowIdx]
        RUID_List.append(workingRUID)
    return RUID_List

df = pd.read_excel("abcd_rucdr_master_forPython.xlsx")
print ('Finished reading in input file.')

#blackList=['NDAR_INV']
#for pattern in blackList:
#    df['pGUID_Rutgers'] = df['pGUID_Rutgers'].replace(pattern, '')
    
#datasets
Mismatch_DAIC_IDs = df.iloc[1949:2201,0].dropna()
print (Mismatch_DAIC_IDs)
Mismatch_Rutgers_IDs = df.iloc[1949:2201,1].dropna()
print (Mismatch_Rutgers_IDs)
Unique_DAIC_IDs = df.iloc[1403:1948,0].dropna()
print (Unique_DAIC_IDs)
Unique_Rutgers_IDs = df.iloc[0:1403,1].dropna()
print (Unique_Rutgers_IDs)
AllRutgersIDs = df['rucdr.SUBCODE'].dropna()
AllDAIC_IDs = df['abcd.id_redcap'].dropna()



print ('About to start first match2collections.') 
BestMatch_Mismatch_DtoR, BestScore_Mismatch_DtoR, BestRowIdx_Mismatch_DtoR = match2Lists(Mismatch_DAIC_IDs,AllRutgersIDs)
print ('Just finished first match2collections.') 
print ('About to start second match2collections.') 
BestMatch_Mismatch_RtoD, BestScore__Mismatch_RtoD, BestRowIdx_Mismatch_RtoD = match2Lists(Mismatch_Rutgers_IDs, AllDAIC_IDs)
print ('Just finished second match2collections.') 
print ('About to start third match2collections.') 
BestMatch_Unique_DtoR, BestScore_Unique_DtoR, BestRowIdx_Unique_DtoR = match2Lists(Unique_DAIC_IDs, AllRutgersIDs)
print ('Just finished third match2collections.') 
print ('About to start fourth match2collections.') 
BestMatch_Unique_RtoD, BestScore_Unique_RtoD, BestRowIdx_Unique_RtoD = match2Lists(Unique_Rutgers_IDs, AllDAIC_IDs)
print ('Just finished fourth match2collections.') 
 
df['BestMatchdf_Mismatch_DtoR']=pd.Series(BestMatch_Mismatch_DtoR)
df['BestScoredf_Mismatch_DtoR']=pd.Series(BestScore_Mismatch_DtoR)
df['BestRowIdxdf_Mismatch_DtoR']=pd.Series(BestRowIdx_Mismatch_DtoR)
df['BestMatchdf_Mismatch_RtoD']=pd.Series(BestMatch_Mismatch_RtoD)
df['BestScoredf_Mismatch_RtoD']=pd.Series(BestScore__Mismatch_RtoD)
df['BestRowIdxdf_Mismatch_RtoD']=pd.Series(BestRowIdx_Mismatch_RtoD)

df['BestMatchdf_Unique_DtoR']=pd.Series(BestMatch_Unique_DtoR)
df['BestScoredf_Unique_DtoR']=pd.Series(BestScore_Unique_DtoR)
df['BestRowIdxdf_Unique_DtoR']=pd.Series(BestRowIdx_Unique_DtoR)
df['BestMatchdf_Unique_RtoD']=pd.Series(BestMatch_Unique_RtoD)
df['BestScoredf_Unique_RtoD']=pd.Series(BestScore_Unique_RtoD)
df['BestRowIdxdf_Unique_RtoD']=pd.Series(BestRowIdx_Unique_RtoD)

InvCode_Mismatch_DtoR_List = createRUID_List(BestRowIdx_Mismatch_DtoR, 'Inventory_Code')
df['InvCode_Mismatch_DtoR']=pd.Series(InvCode_Mismatch_DtoR_List)
InvCode_Mismatch_RtoD_List = createRUID_List(BestRowIdx_Mismatch_RtoD, 'Inventory_Code')
df['InvCode_Mismatch_RtoD']=pd.Series(InvCode_Mismatch_RtoD_List)
 
InvCode_Unique_DtoR_List = createRUID_List(BestRowIdx_Unique_DtoR, 'Inventory_Code')
df['InvCode_Unique_DtoR']=pd.Series(InvCode_Unique_DtoR_List)
InvCode_Unique_RtoD_List = createRUID_List(BestRowIdx_Unique_RtoD, 'Inventory_Code')
df['InvCode_Unique_RtoD']=pd.Series(InvCode_Unique_RtoD_List)

writer = pd.ExcelWriter('FuzzyMatchedIDsOne_190730.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()

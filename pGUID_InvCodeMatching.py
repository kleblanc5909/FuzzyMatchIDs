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
    TopMatches = []
    TopScores = []
    TopRowIdxs = []
    for member in list1:
        x=process.extract(member, list2)
        TopMatches.append(x[0,3,6])
        TopScores.append(x[1,4,7])
        TopRowIdxs.append(x[2,5,8])
    return TopMatches, TopScores, TopRowIdxs

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
Unique_DAIC_Invs = df['InvCodeDAIC_OnlyTxt'].dropna()
Unique_Rutgers_Invs = df['InvCodeRUCDR_OnlyTxt'].dropna()
AllRutgersInvs = df['InvCodeMinusDOTxt'].dropna()
AllDAIC_Invs = df['InvCodeMinusROTxt'].dropna()



print ('About to start first match2collections.') 
BestMatch_DtoR, BestScore_DtoR, BestRowIdx_DtoR = match2Lists(Unique_DAIC_Invs,AllRutgersInvs)
print ('Just finished first match2collections.') 
print ('About to start second match2collections.') 
BestMatch_RtoD, BestScore_RtoD, BestRowIdx_RtoD = match2Lists(Unique_Rutgers_Invs, AllDAIC_Invs)
print ('Just finished second match2collections.') 
#print ('About to start third match2collections.') 
#BestMatch_DtoD, BestScore_DtoD, BestRowIdx_DtoD = match2Lists(Unique_DAIC_IDs, AllDAIC_IDs)
#print ('Just finished third match2collections.') 
#print ('About to start fourth match2collections.') 
#BestMatch_RtoR, BestScore_RtoR, BestRowIdx_RtoR = match2Lists(Unique_Rutgers_IDs, AllRutgersIDs)
#print ('Just finished fourth match2collections.') 
 
df['BestMatchdf_DtoR']=pd.Series(BestMatch_DtoR)
df['BestScoredf_DtoR']=pd.Series(BestScore_DtoR)
df['BestMatchdf_RtoD']=pd.Series(BestMatch_RtoD)
df['BestScoredf_RtoD']=pd.Series(BestScore_RtoD)
df['BestRowIdxdf_DtoR']=pd.Series(BestRowIdx_DtoR)
df['BestRowIdxdf_RtoD']=pd.Series(BestRowIdx_RtoD)

#df['BestMatchdf_DtoD']=pd.Series(BestMatch_DtoD)
#df['BestScoredf_DtoD']=pd.Series(BestScore_DtoD)
#df['BestMatchdf_RtoR']=pd.Series(BestMatch_RtoR)
#df['BestScoredf_RtoR']=pd.Series(BestScore_RtoR)
#df['BestRowIdxdf_DtoD']=pd.Series(BestRowIdx_DtoD)
#df['BestRowIdxdf_RtoR']=pd.Series(BestRowIdx_RtoR)

pGUID_DtoR_List = createRUID_List(BestRowIdx_DtoR, 'rucdr.SUBCODE')
df['pGUID_DtoR']=pd.Series(pGUID_DtoR_List)
pGUID_RtoD_List = createRUID_List(BestRowIdx_RtoD, 'abcd.id_redcap')
df['pGUID_RtoD']=pd.Series(pGUID_RtoD_List)
 
#RUID_DtoD_List = createRUID_List(BestRowIdx_DtoD, 'RUID_DAIC')
#df['RUID_DtoD']=pd.Series(RUID_DtoD_List)
#KCode_DtoD_List = createRUID_List(BestRowIdx_DtoD, 'Kim_code')
#df['KCode_DtoD']=pd.Series(KCode_DtoD_List)
#RUID_RtoR_List = createRUID_List(BestRowIdx_RtoR, 'RUID_Rutgers')
#df['RUID_RtoR']=pd.Series(RUID_RtoR_List)

writer = pd.ExcelWriter('FuzzyMatchedInvsOne.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()

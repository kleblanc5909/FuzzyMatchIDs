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

df = pd.read_excel("DataReleaseMismatches.xlsx",sheet_name = "Sheet3")
print ('Finished reading in input file.')

#blackList=['NDAR_INV']
#for pattern in blackList:
#    df['pGUID_Rutgers'] = df['pGUID_Rutgers'].replace(pattern, '')
    
#datasets
DR_DAIC_pGUIDs = df['pGUID_DAIC'].dropna()
Current_DAIC_pGUIDs = df['abcd.id_redcap'].dropna()




print ('About to start first match2collections.') 
BestMatch_DRtoC, BestScore_DRtoC, BestRowIdx_DRtoC = match2Lists(DR_DAIC_pGUIDs, Current_DAIC_pGUIDs)
print ('Just finished first match2collections.') 
#print ('About to start second match2collections.') 
#BestMatch_RtoD, BestScore_RtoD, BestRowIdx_RtoD = match2Lists(Unique_Rutgers_Invs, AllDAIC_Invs)
#print ('Just finished second match2collections.') 
#print ('About to start third match2collections.') 
#BestMatch_DtoD, BestScore_DtoD, BestRowIdx_DtoD = match2Lists(Unique_DAIC_IDs, AllDAIC_IDs)
#print ('Just finished third match2collections.') 
#print ('About to start fourth match2collections.') 
#BestMatch_RtoR, BestScore_RtoR, BestRowIdx_RtoR = match2Lists(Unique_Rutgers_IDs, AllRutgersIDs)
#print ('Just finished fourth match2collections.') 
 
df['BestMatchdf_DRtoC']=pd.Series(BestMatch_DRtoC)
df['BestScoredf_DRtoC']=pd.Series(BestScore_DRtoC)
df['BestRowIdxdf_DRtoC']=pd.Series(BestRowIdx_DRtoC)

#df['BestMatchdf_DtoD']=pd.Series(BestMatch_DtoD)
#df['BestScoredf_DtoD']=pd.Series(BestScore_DtoD)
#df['BestMatchdf_RtoR']=pd.Series(BestMatch_RtoR)
#df['BestScoredf_RtoR']=pd.Series(BestScore_RtoR)
#df['BestRowIdxdf_DtoD']=pd.Series(BestRowIdx_DtoD)
#df['BestRowIdxdf_RtoR']=pd.Series(BestRowIdx_RtoR)

pGUID_DRtoC_List = createRUID_List(BestRowIdx_DRtoC, 'MismatchCode')
df['pGUID_DRtoC']=pd.Series(pGUID_DRtoC_List)

 
#RUID_DtoD_List = createRUID_List(BestRowIdx_DtoD, 'RUID_DAIC')
#df['RUID_DtoD']=pd.Series(RUID_DtoD_List)
#KCode_DtoD_List = createRUID_List(BestRowIdx_DtoD, 'Kim_code')
#df['KCode_DtoD']=pd.Series(KCode_DtoD_List)
#RUID_RtoR_List = createRUID_List(BestRowIdx_RtoR, 'RUID_Rutgers')
#df['RUID_RtoR']=pd.Series(RUID_RtoR_List)

writer = pd.ExcelWriter('DRMatchedpGUIDsOne.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()

# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 18:23:56 2018

@author: Lab
"""
import numpy as np
import sys
## input files and output file locations
itcount_file=sys.argv[1]
percentile_file=sys.argv[2]
repeat_donors_file=sys.argv[3]
## read input file
def Read_Files(filename):
    f = open(filename,'r')
    lines = f.readlines()
    f.close()
    return lines
##When every line of data is called, get needed features and store it data dictionary
def Get_Data(line):
    data={}
    CMTE_ID=line.split('|')[0].strip()
    NAME=line.split('|')[7].strip()
    ZIP_CODE=line.split('|')[10].strip()
    TRANSACTION_DT=line.split('|')[13].strip()
    TRANSACTION_AMT=line.split('|')[14].strip()
    OTHER_ID=line.split('|')[15].strip()
    data={'CMTE_ID':CMTE_ID,'NAME':NAME,'ZIP_CODE':ZIP_CODE,'TRANSACTION_DT':TRANSACTION_DT,'TRANSACTION_AMT':
        TRANSACTION_AMT,'OTHER_ID':OTHER_ID}
    return data   
## check input data obey the rules, make two new features : ID_DONOR, ID_UNIQUE_CMTE and export cleaned data
def Clean_Data(data):
    # digitparam: the array that we expect to be digits
    digitparam=['ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT']
    # rules: other Id must be empty, zip_code must be at least five digits, Date must be 8 digits
    rules=[len(data['OTHER_ID'])==0,len(data['ZIP_CODE'])>4,len(data['TRANSACTION_DT'])==8]
    # loop on data keys
    for key in data.keys():
        # check if features in digitparam are digits 
        if key in digitparam:rules.append(data[key].isdigit())
        # check if other_id is only empty and the rest of features have some value
        if key!='OTHER_ID': rules.append(len(data[key])>0)
    #if input data obey the rules, so data are clean and make new features, if not, report empty data 
    if all(rules):
        # store only first five digits of zip_code
        ZIP_CODE=data['ZIP_CODE'][0:5]
        # store year from 'TRANSACTION_DT'
        YEAR=data['TRANSACTION_DT'][4:8]
        # make new feature with zip_code and name and call it ID_DONOR (if this feature is the same for two donors they are the same) 
        ID_DONOR=ZIP_CODE+data['NAME']
         # make new feature with year, zip_code and 'CMTE_ID' and call it ID_UNIQUE_CMTE (if this feature is the same for two recepient they are the same resepient. Year is added to do next calculation per year) 
        ID_UNIQUE_CMTE=YEAR+ZIP_CODE+data['CMTE_ID']
        # add new features to data and round 'TRANSACTION_AMT'  
        data['ZIP_CODE'],data['TRANSACTION_DT'],data['ID_DONOR'],data['ID_UNIQUE_CMTE'],data['TRANSACTION_AMT']=ZIP_CODE, int(YEAR), ID_DONOR,ID_UNIQUE_CMTE,np.round(float(data['TRANSACTION_AMT']))
    else:
        data={}
    return data    
# check the donor is a repeat donor or not
def Find_Repeat_Donor(ID_DONOR,YEAR,donors):
    # check if the new donor (ID_DONOR) is in donors dictionary and he/she has contributed in the prior years
    # if not store (ID_DONOR) in the donor dictionary
    # REPEAT_DONOR: True if he is a repeat donor, otherwise False
    if ID_DONOR in donors.keys():
        REPEAT_DONOR=(donors[ID_DONOR]<=YEAR)
        donors[ID_DONOR]=min(donors[ID_DONOR],YEAR)
    else:
        donors[ID_DONOR]=YEAR
        REPEAT_DONOR=False
    return REPEAT_DONOR,donors
#save amount of contribution by repeat donors as an array for every ID_UNIQUE_CMTE in the recipient dictionary 
def Save_Recipient(recipient,ID_UNIQUE_CMTE,AMT):
    if ID_UNIQUE_CMTE in recipient.keys():
        recipient[ID_UNIQUE_CMTE].append(AMT)
        recipient[ID_UNIQUE_CMTE]=sorted(recipient[ID_UNIQUE_CMTE])
    else:
        recipient[ID_UNIQUE_CMTE]=[AMT]
    return recipient 
# calculate number of contributions, summation and percentile
#  AMT_List : list of amount of contributions by repeat_donors per year for every unique recepient 
def Make_Output(AMT_List,percentile):
    n=len(AMT_List)
    percentile_value=AMT_List[int(np.ceil(n*percentile/100))-1]
    sum_value=sum(AMT_List)
    return int(percentile_value), int(sum_value),n
                             
#keys: data['ID_DONOR']=ZIP_CODE+Name    Values: Minimum year that he/she has contributed 
donors={}   
# keys: unique recepients in every year (data['ID_UNIQUE_CMTE']), Values: a list of contributions by repeat donors 
recipient={} 
# all of data read in a sigle line will be stored in data
data={} 
#read input file "itcount.txt" and store lines 
lines=Read_Files(itcount_file)
#read input file "percentile.txt" and store percentile
PERCENTILE=float(Read_Files(percentile_file)[0])
#open output file and write if following conditions are met
with open(repeat_donors_file,'w') as file:
    # read input file line by line
    for line in lines:
        # get data for every line and store it in the data dictionary
        data=Get_Data(line)
        # clean data and make new features
        data=Clean_Data(data)
        # if coniditions are not met, read the next line
        if bool(data)==False:continue
        #is_repeat_donor: reprort True if he/she is a repeat donors
        #make donor dictionary: store 'ID_DONOR' and 'TRANSACTION_DT  
        is_repeat_donor,donors=Find_Repeat_Donor(data['ID_DONOR'],data['TRANSACTION_DT'],donors)
        #if he/she is not repeat_donor read the line of input data
        if is_repeat_donor==False:continue
        #make recepient dictionary : store amount of transaction of repeat_donors for unique recepient
        recipient=Save_Recipient(recipient,data['ID_UNIQUE_CMTE'],data['TRANSACTION_AMT'])
        # calculate number,summation and percentile of contributions
        [PERCENTILE_VALUE, SUM_VALUE,N]=Make_Output(recipient[data['ID_UNIQUE_CMTE']],PERCENTILE)
        # write the on the output file
        file.write('{0}|{1}|{2}|{3}|{4}|{5}\n'.format(data['CMTE_ID'],data['ZIP_CODE'],data['TRANSACTION_DT'],PERCENTILE_VALUE,SUM_VALUE,N))


    



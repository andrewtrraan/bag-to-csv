



import psycopg2
import pandas as pd
import numpy as np
from psycopg2 import sql
import json
import csv
import pprint as pp
import time 
import argparse
import os



#takes in arguments to flatten data column to csv
parser = argparse.ArgumentParser(description ='Enter the fields')
parser.add_argument('-l','--limit', dest='limit', type=str, default='10', help ='limit of database entries')
parser.add_argument('-o','--offset', dest='offset', type=str, default='0', help='offset value')
parser.add_argument('-db','--database-name', dest ='db', required=True, type=str, help ='name of database')
parser.add_argument('-ho','--host', dest ='ho',type=str,default= "compute1.esg.uwaterloo.ca", help ='name of database')
parser.add_argument('-u','--user', dest='user', type=str,default="esgdata", help='user name')
parser.add_argument('-p','--password', dest='pw',type=str, default="esg2016data",help='account password')
parser.add_argument('-t','--table-name',dest='table_name',required =True,type=str, help='Table to read from')
arguments = parser.parse_args()

#gets the diretory name of where the scirpt is currently running
cur_dir = os.getcwd()

#changes the name of the bag file to match bag file csv
real_table = arguments.table_name

#name of the flattened csv
f_name = real_table.replace('_json','_csv')+".csv"

#opens connection
con = psycopg2.connect(host=arguments.ho, dbname=arguments.db, user=arguments.user, password=arguments.pw)


#the file location
file_location = cur_dir +'/' +f_name


#reads in the data column from database to dataframe then converts to dictionary
s2 ="SELECT data FROM "+real_table
df2= pd.read_sql(s2,con)
to_j = df2.to_dict()


#function that generates the rows of the csv file
def flat(data,parent,a_dict):
    #holds the entire family name if nested 
    root = parent 

    #skip because empty
    # if data is None:
    #     return ''
    
    #loop through the json object
    for key in data: 

        #if the value at the current key is type dict
        if type(data[key])==dict:

            #concatenate the current family name with the next key
            parent = root + '_' + key

            #recurse until reach the end of family tree at child
            flat(data[key],parent,a_dict)

        #if there is a nested list object as the child
        elif type(data[key])==list:

            #NOTE THIS STARTS AT INDEX 1 NOT INDEX 0 IN THE NAMING
            for j in range(0, len(data[key])):
                lst=data[key]
                ins = root+'_'+key+'_'+str(j+1)
                
                #add the child with entire name to row
        

                a_dict.update({ins:lst[j]})
        
        #if traversed entire family tree and at child
        else:
            #add the child with the correct family name to row
            ins=root + '_' + key
            
            a_dict.update({ins:data[key]})           

    #return the row 
    return a_dict

#function that generates the column headers of csv file
#DOES SAME THING AS ABOVE FUNCTION BUT INSTEAD APPENDS UNIQUE COLUMN HEADERS TO A LIST INSTEAD OF PUTTING INTO DICTIONARY FOR ROW
def get_name(data,parent,pass_lst): 

    #holds the entire family name if nested 
    root = parent 
    
    #skip because empty
    # if data is None:
    #     return ''

    #loop through the json object
    for key in data: 

        #if the value at the current key is type dict
        if type(data[key])==dict:
            parent = root + '_' + key
            get_name(data[key],parent,pass_lst)
        elif type(data[key])==list:
            for j in range(0, len(data[key])):
                lst=data[key]
                ins = root+'_'+key+'_'+str(j+1)
                if ins not in temp_lst:
                    pass_lst.append(ins)
        else:
            ins=root + '_' + key
            if ins not in temp_lst:
                pass_lst.append(ins)








#getting all the column headers
temp_lst=[]
for i in range(0,len(to_j['data'])):
    curr_object=to_j['data'][i]

    g=get_name(curr_object,'',temp_lst)


str0 = cur_dir +'/' +arguments.table_name.replace('_json','_csv')+'_db_str0.txt'
str1 = cur_dir +'/' +arguments.table_name.replace('_json','_csv')+'_db_str1.txt'
#writing the text file for dumping script
db_str=''
for i in range(0,len(temp_lst)-1):
    entry =temp_lst[i]+" character varying,\n"
    db_str+=entry
db_str+=(temp_lst[len(temp_lst)-1]+" character varying")


file = open(str0,"w")
file.write(db_str)
file.close()

#writing the text file for the dumping script

db_str1=''
for i in range(0,len(temp_lst)-1):
    entry =temp_lst[i]+','
    db_str1+=entry

db_str1+=(temp_lst[len(temp_lst)-1])


file = open(str1,"w")
file.write(db_str1)
file.close()



#writing the csv file
with open(file_location,'w') as csvfile:
    fieldnames=temp_lst
    writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
    writer.writeheader()

    #looping through entire date column
    for i in range(0,len(to_j['data'])):
        d1={}
        curr_object=to_j['data'][i]
        f=flat(curr_object,'',d1)
        writer.writerow(f)



#putting the final csv into the database

import psycopg2
from psycopg2 import sql
import os 
import argparse



#takes in arguments to dump flattened json csv into datbase
parser = argparse.ArgumentParser(description ='Enter the fields')
parser.add_argument('-db','--database-name', dest ='db', required=True, type=str, help ='name of database')
parser.add_argument('-ho','--host', dest ='ho',type=str, help ='name of database')
parser.add_argument('-u','--user', dest='user', type=str,help='user name')
parser.add_argument('-p','--password', dest='pw',type=str, help='account password')
parser.add_argument('-fj','--flattened-json',dest='flatted_json',required =True,type=str, help='Name of flattened json file')
arguments = parser.parse_args()


#gets the diretory name of where the scirpt is currently running
cur_dir = os.getcwd()

#manipulates bag name to match flattened json file name
temp=arguments.flatted_json.replace(".bag","_csv.csv")
f_path = cur_dir + "/output/" + temp
_csv = temp.replace(".csv","")

#opens the the flattened json
file = open(f_path,'r')

str0 = cur_dir +'/output/' +arguments.flatted_json.replace('.bag','_db_str0.txt')
str1 = cur_dir +'/output/' +arguments.flatted_json.replace('.bag','_db_str1.txt')

#reads in the text file with the column names generated from the flattener script
read_in =open(str0,"r")
dbstr=''
for line in read_in:
    dbstr+=line
read_in1 =open(str1,"r")
dbstr1=''
for line in read_in1:
    dbstr1+=line


#opens connection
con1 = psycopg2.connect(host=arguments.ho, dbname=arguments.db, user=arguments.user, password=arguments.pw)
cur =con1.cursor()

#generates table
cur.execute("CREATE TABLE {} ({});".format(_csv,dbstr))



con1.commit()

cur.copy_expert("COPY {} ({}) FROM STDIN DELIMITER ',' CSV HEADER;".format(_csv,dbstr1), file)


con1.commit()




#os.remove("db_str.txt")
#os.remove("db_str1.txt")


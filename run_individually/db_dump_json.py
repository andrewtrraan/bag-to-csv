

#putting name_json.csv form of bag file into database
import psycopg2
from psycopg2 import sql
import os
import argparse



#takes in arguments to dump bag file csv into datbase
parser = argparse.ArgumentParser(description ='Enter the fields')
parser.add_argument('-db','--database-name', dest ='db', required=True, type=str, help ='name of database')
parser.add_argument('-ho','--host', dest ='ho',type=str, help ='name of database')
parser.add_argument('-u','--user', dest='user', type=str, help='user name')
parser.add_argument('-p','--password', dest='pw',type=str, help='account password')
parser.add_argument('-bc','--bag-csv-name',dest='bag_csv',required =True,type=str, help='Name of bag csv file')
arguments = parser.parse_args()


#gets the diretory name of where the scirpt is currently running
cur_dir = os.getcwd()

#manipulates bag name to match bag file csv file name
in_bag = arguments.bag_csv
f_path = cur_dir + "/" + in_bag

#opens the connection
con1 = psycopg2.connect(host=arguments.ho, dbname=arguments.db, user=arguments.user, password=arguments.pw)
cur =con1.cursor()

#name of the databse table
input_table = in_bag.replace('.csv','')



#creates database table 
file = open(f_path, "r")
cur.execute("CREATE TABLE {}(timestamp bigint,object_type character varying,data jsonb);".format(input_table))
#cur.execute("CREATE TABLE {}(timestamp bigint,object_type character varying,data character varying);".format(input_table))


con1.commit()

#copies csv file into database
cur.copy_expert("COPY {}(timestamp,object_type,data) FROM STDIN DELIMITER ','  CSV HEADER;".format(input_table), file)



con1.commit()

print(f_path)

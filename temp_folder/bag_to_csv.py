
import rosbag 
import csv
from std_msgs.msg import Int32, String
import argparse
import json
import yaml
import os
import re
from yaml import CLoader as Loader, CDumper as Dumper



#reads in name of bag file
parser = argparse.ArgumentParser(description ='Enter the fields')
parser.add_argument('-bn','--bag-name', dest='bag_name', type=str, default='cheese', help ='name of the bag')
arguments = parser.parse_args()

#gets rosgbag
bag = rosbag.Bag(arguments.bag_name)

#maniplates filename so it will be in filename_json.csv format
file_name = arguments.bag_name.replace('.bag','_json')+".csv"

#headers for csv file
headers= ['timestamp','object_type','data']

#gets the diretory name of where the scirpt is currently running
cur_dir = os.getcwd()

file_location = cur_dir+'/output/'+file_name

#write the csv file



#fh = open('cheese.txt','wr')
#write the csv file
with open(file_location,'w') as csvfile:
    fieldnames=headers
    #writer=csv.DictWriter(csvfile,fieldnames=fieldnames,lineterminator='\n',escapechar='\\',quoting=csv.QUOTE_NONE)
    writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
    writer.writeheader()
    for topic,msg, t in bag.read_messages():
        a_dict={}

        #updates the dicionary that will hold row entry
        a_dict.update({'timestamp':str(t)})
        a_dict.update({'object_type':str(topic).replace('/','_')})



        #converts the data column to json format
        data = yaml.load(str(msg), Loader=Loader)
        #y= yaml.load(str(msg))
        put_in = json.dumps(data,indent=4)
        a_dict.update({'data':str(put_in)})
        writer.writerow(a_dict)     





bag.close()


NOTE: db_dump_csv.py cannot run unless json_parser.py is ran first 
==================================================================

NOTE: in json_parser.py when there is a nested list for one of the values the names are starting at 1 not 0 
Example:

cheese =[0,0,0]

In the csv it would look like
cheese_1 , cheese_2, cheese_3
0          0         0

**REQUIREMENTS BEFORE RUNNING SCRIPT:**
- MAKE SURE TABLE DOES NOT ALREADY EXIST IN DATABASE
- MAKE SURE YOUR USER IS ADDED TO THE DOCKER GROUP AND THAT DOCKER IS INSTALLED 
- MAKE SURE YOUR DESIRED BAG FILE IS ADDED TO THE SAME DIRECTORY AS THE SCRIPTS
- MAKE SURE ROS KINETIC IS INSTALLED IF NOT USING DOCKER

-ALL GENERATED FILES WILL BE STORED IN THE OUPUT FOLDER AT THE END-




RUN last_2.sh if you want to just pull from a _json table and flatten then push it bag into database.

DOCKER STEPS:
=============

1. BUILD THE DOCKER FILE (docker build -t my-app .)
2. RUN THE DOCKER FILE AND MOUNT THE VOLUME SO OUTPUT WILL BE CORRECTLY STORED (docker run -it -v $(pwd)/temp_folder:/home/tmp1 my-app:latest)
3. EXAMPLE OF RUNNING ON COMPUTE2 BECASUE SELINUX RESTRICTIONS:

docker run -it -v $(pwd)/temp_folder:/home/tmp1:Z fruit-loops:latest




HOW TO RUN SCRIPT:
==================
**5 PARAMETERS MUST BE PASSED IN TO RUN THE SCRIPT:**

- DATABASE NAME
- DATABASE HOST
- DATABASE USER
- DATABASE PASSWORD
- BAGFILE NAME

(MUST BE IN THAT EXACT ORDER)

EXAMPLE OF HOW TO RUN THE SCRIPT

./automate.sh database_name database_host database_user database_password bag_file_name

./automate.sh postgres 127.0.0.1 postgres password testing_.bag

HOW TO RUN THE SCRIPTS INDIVIDUALLY:
====================================


1. bag_to_csv.py

python2 -bn _the_bag_name


2. db_dump_json.py

NOTE: ending of file must be filename_json.csv format

python3 -db _database_name -ho _host_name -u _database_user -p _database_user_password -bc _name_of_bag_csv


3. json_parser.py

python3 -db _database_name -ho _host_name -u _database_user -p _database_user_password -t _table_to_convert

4. db_dump_csv.py

python3 -db _database_name -ho _host_name -u _database_user -p _database_user_password -fj _name_of_flattened_json_in_csv






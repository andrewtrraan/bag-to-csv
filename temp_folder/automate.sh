
#!/bin/sh

DB_NAME="$1"
DB_HOST="$2"
DB_USER="$3"
DB_PW="$4"
BAG_NAME="$5"


chmod +x bag_to_csv.py
python2 bag_to_csv.py -bn "$5"
echo "DONE BAG TO CSV"

chmod +x db_dump_json.py
python3 db_dump_json.py -db "$1" -ho "$2" -u "$3" -p "$4" -bc "$5"
echo "BAG FILE CSV IN DB"

chmod +x json_parser.py
python3 json_parser.py -db "$1" -ho "$2" -u "$3" -p "$4" -t "$5"
echo "CONVERTED DATA COLUMN FROM DB TO CSV"

chmod +x db_dump_csv.py
python3 db_dump_csv.py -db "$1" -ho "$2" -u "$3" -p "$4" -fj "$5"
echo "FLATTENED JSON IN DB"

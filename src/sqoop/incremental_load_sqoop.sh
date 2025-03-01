## Before run this script do full load to source database to hdfs
##sqoop import --connect jdbc:postgresql://18.132.73.146:5432/testdb --username consultants --password WelcomeItc@2022 --table hitesh_employee --m 1 --target-dir /tmp/bigdata_nov_2024/hitesh/feb2025/employee_full_load/
##
##
## # To list the column names of a table
# SELECT column_name
# FROM information_schema.columns
# WHERE table_schema = 'public'  -- Replace with your schema name if it's different
#  AND table_name   = 'table';  -- Replace with your table name
# TO CREATE EXTERNAL TABLE >> FULL LOAD
# Put this code in Hive GUI
# CREATE EXTERNAL TABLE hitesh_itc.hitesh_employee (
    id int, name char(100), phone_number char(20), department char(50), salary int
# )
# ROW FORMAT DELIMITED
# FIELDS TERMINATED BY ','  
# LINES TERMINATED BY '\n'  
# STORED AS TEXTFILE
# LOCATION ' /tmp/bigdata_nov_2024/hitesh/feb2025/employee_full_load/


#!/bin/bash

# Variables
HOSTNAME="18.132.73.146"
DBNAME="testdb"
USERNAME="consultants"
PASSWORD="WelcomeItc@2022"
TABLE="hitesh_employee"
HDFS_DIR="'/tmp/bigdata_nov_2024/hitesh/feb2025/employee_full_load/"
HIVE_DATABASE="hitesh_itc"
HIVE_TABLE="hitesh_employee"
HIVE_URL="jdbc:hive2://ip-172-31-1-36.eu-west-2.compute.internal:10000/${HIVE_DATABASE}"

# Fetch the maximum id value from Hive
LAST_VALUE=$(beeline -u "jdbc:hive2://ip-172-31-1-36.eu-west-2.compute.internal:10000/hitesh_itc;" --silent=true -e "SELECT MAX(id)
 FROM ${TABLE};" | grep -o '[0-9]*' | tail -n 1)
echo "Last recorded ID from Hive: $LAST_VALUE"
echo "Starting new import from ID greater than $LAST_VALUE"

# Perform the incremental Sqoop import
sqoop import --connect jdbc:postgresql://18.132.73.146:5432/testdb --username consultants --password WelcomeItc@2022 --table hitesh_employee --m 1 --target-dir /tmp/bigdata_nov_2024/hitesh/feb2025/employee_full_load -m 1 --incremental append --check-column id --last-value $LAST_VALUE --as-textfile

# Check if the Sqoop import was successful
if [ $? -eq 0 ]; then
    echo "Sqoop Incremental Import Successful"
    
    # Check if the HDFS directory has data
    HDFS_COUNT=$(hdfs dfs -count ${HDFS_DIR} | awk '{print $2}')
    if [ $HDFS_COUNT -gt 0 ]; then
        echo "New data found in HDFS directory: ${HDFS_DIR}"
        
        # Load new data into Hive table
        echo "Loading new data into Hive table: ${HIVE_DATABASE}.${HIVE_TABLE}"
        beeline -u "${HIVE_URL}" \
          -e "LOAD DATA INPATH '${HDFS_DIR}' INTO TABLE ${HIVE_DATABASE}.${HIVE_TABLE};"
        
        echo "Data successfully loaded into Hive table: ${HIVE_DATABASE}.${HIVE_TABLE}"
    else
        echo "No new data found in HDFS directory: ${HDFS_DIR}"
    fi
else
    echo "Sqoop Incremental Import Failed"
    exit 1
fi
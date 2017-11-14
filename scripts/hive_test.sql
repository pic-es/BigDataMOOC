# ------------------------------ CREATE TABLE ------------------------------
CREATE TABLE IF NOT EXISTS weather(
STATION STRING,
STATION_NAME STRING,
WDATE STRING,
AWND FLOAT,
PGTM FLOAT,
PRCP FLOAT,
SNOW FLOAT,
SNWD FLOAT,
TAVG FLOAT,
TMAX FLOAT,
TMIN FLOAT,
WDF2 FLOAT,
WDF5 FLOAT,
WESD FLOAT,
WESF FLOAT,
WSF2 FLOAT,
WSF5 FLOAT,
WT01 FLOAT,
WT02 FLOAT,
WT03 FLOAT,
WT04 FLOAT,
WT06 FLOAT,
WT08 FLOAT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");
;

# ------------------------------ LOAD CSV FILE TO HIVE TABLE ------------------------------
LOAD DATA LOCAL INPATH '/home/cloudera/BigDataMOOC/data/weather_data.csv' OVERWRITE INTO TABLE weather;

# ------------------------------ TEST QUERY (EXPECTED RESULT = 7117) ------------------------------
SELECT COUNT(*) FROM weather;


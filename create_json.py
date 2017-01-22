import Admin
import MySQLdb as mdb

import datetime
import time
import json

query24hour = """SELECT bmp180.hourMeasured, bmp180.timeBlock, bmp180.temperature_f,
bmp180.barometric_pressure, dht22.humidity, bmp180.dateMeasured
FROM bmp180 INNER JOIN dht22 on bmp180.reading_id = dht22.reading_id
ORDER BY hourMeasured DESC LIMIT 48;"""

query5days = """SELECT dateMeasured, timeBlock, AVG(temperature_f), AVG(barometric_pressure), AVG(humidity)
FROM (SELECT bmp180.dateMeasured, bmp180.timeBlock, bmp180.temperature_f,
bmp180.barometric_pressure, dht22.humidity
FROM bmp180 INNER JOIN dht22 on bmp180.reading_id = dht22.reading_id
LIMIT 240 ) AS subTable GROUP BY dateMeasured, timeBlock LIMIT 30;"""

# Query the databases

def select24():
    con=mdb.connect(Admin.MySQLCredentials.host, Admin.MySQLCredentials.user, Admin.MySQLCredentials.password, Admin.MySQLCredentials.database)

    with con:
        cur=con.cursor()
        cur.execute(query24hour)

        return cur.fetchall()

def select5Days():
    con=mdb.connect(Admin.MySQLCredentials.host, Admin.MySQLCredentials.user, Admin.MySQLCredentials.password, Admin.MySQLCredentials.database)

    with con:
        cur=con.cursor()
        cur.execute(query5days)

        return cur.fetchall()


lastDay = select24()
lastFive = select5Days()


# Transform the data to JSON formats
def reshape_last_day(data):
    json_data = []
    for row in data:
        outrow = {"timestamp": row[0],
                  "timeblock": row[1],
                  "temp_f": row[2], 
                  "bmp": row[3],
                  "humidity": row[4], 
                  "date": row[5]}
        json_data.append(outrow)
    return json_data

lastDay = reshape_last_day(lastDay)

def reshape_last_five(data):
    json_data = []
    for row in data:
        outrow = {"date": row[0],
                  "timeblock": row[1],
                  "avg_temp_f": row[2],
                  "avg_bmp": row[3],
                  "avg_humidity": row[4]}
        json_data.append(outrow)
    return json_data

lastFive = reshape_last_five(lastFive)


# Transform the dates and times to be JSON-readable
def serialize_timeobject(obj):
    if isinstance(obj, (datetime.date, datetime.time, datetime.datetime)):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

def update_time(data):
    for row in data:
        if "timestamp" in row:
            row["timestamp"] = serialize_timeobject(row["timestamp"])
        if "date" in row:
            row["date"] = serialize_timeobject(row["date"])


for data in [lastDay, lastFive]:
    update_time(data)


#print(lastDay)

# Store as json document
lastDay = json.dumps(lastDay)
with open("PiWebApp/WeatherDash/lastDay.json", "w") as outfile:
    outfile.write(lastDay)

lastFive = json.dumps(lastFive)
with open("PiWebApp/WeatherDash/lastFive.json", "w") as outfile:
    outfile.write(lastFive)


# Loading the JSON from a file
#with open('json/tenData.json') as json_data:
#    d = json.load(json_data)

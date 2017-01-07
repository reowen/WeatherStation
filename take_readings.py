
import sys
import time
import datetime
import json
import subprocess
import re
import os
import time

import Admin
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_DHT
import gspread
import MySQLdb as mdb
from oauth2client.service_account import ServiceAccountCredentials

# Set the time of the script being run
time_of_reading = datetime.datetime.now()
print(time_of_reading)
currentDate=time_of_reading.date()

# Calculate 4-hour block for daily averages
midnight=datetime.datetime.combine(time_of_reading.date(),datetime.time())
minutes=((time_of_reading-midnight).seconds)/60 #minutes after midnight, use datead$
block = int(((minutes/60) / 4)) # change the 4 to the desired block length

# Set the DHT Sensor Type and GPIO Pin #
DHT_TYPE = Adafruit_DHT.DHT22
DHT_PIN  = 23

# BMP 180 -- Create sensor instance with default I2C bus
bmp = BMP085.BMP085()

# Take the DHT 22 Humidity Readings ####################
# Try 3 times to get a reading
i = 1
while i < 4:
    humidity_dht, temp_dht = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)
    n = i
    if humidity_dht is None or temp_dht is None:
        time.sleep(2)
        i = i + 1
    else:
        i = 4

# If it fails after 3 tries, just move on
if humidity_dht is None or temp_dht is None:
    print "Failed to get DHT readings"
    temp_dht_f = None
else:
    print 'Got DHT reading in {0:0.1f} attempts'.format(n)
    temp_dht_f = (temp_dht * (1.8)) + 32
    print 'DHT Temperature (C): {0:0.1f} C'.format(temp_dht)
    print 'DHT Temperature (F): {0:0.1f} F'.format(temp_dht_f)
    print 'DHT Humidity: {0:0.1f} %'.format(humidity_dht)
    humidity_dht = round(humidity_dht, 1)
    temp_dht = round(temp_dht, 1)
    temp_dht_f = round(temp_dht_f, 1)


# Take the BMP 180 Barometric Pressure Readings ############
temp_bmp = bmp.read_temperature()
temp_bmp_f = (temp_bmp * (1.8)) + 32
pressure = bmp.read_pressure() * 0.01
altitude = bmp.read_altitude()

print 'BMP Temperature (C): {0:0.1f} C'.format(temp_bmp)
print 'BMP Temperature (F): {0:0.1f} F'.format(temp_bmp_f)
print 'Pressure:    {0:0.1f} hPa'.format(pressure)
print 'Altitude:    {0:0.1f} m'.format(altitude)

temp_bmp = round(temp_bmp, 1)
temp_bmp_f = round(temp_bmp_f, 1)
pressure = round(pressure, 1)
altitude = round(altitude, 1)

"""
# Define the procedure for opening the google sheet ##########################
def login_open_sheet(creds, spreadsheet):
        #Connect to Google Docs spreadsheet and return the first worksheet.
        try:
                scope = ['https://spreadsheets.google.com/feeds']
                credentials = ServiceAccountCredentials.from_json_keyfile_name(creds, scope)
                gc = gspread.authorize(credentials)
                worksheet = gc.open_by_url(spreadsheet).sheet1
                return worksheet
        except:
                print 'Unable to login and get spreadsheet.  Check email, password, spreadsheet name.'
                sys.exit(1)
"""

# Define the procedures for writing to the database #########################
def saveToBMP(temp_bmp,temp_bmp_f,pressure,altitude):

    con=mdb.connect(Admin.MySQLCredentials.host, Admin.MySQLCredentials.user, Admin.MySQLCredentials.password, Admin.MySQLCredentials.database)

    with con:
        cur=con.cursor()
        cur.execute("INSERT INTO bmp180 (temperature_c,temperature_f,barometric_pressure,altitude,dateMeasured,hourMeasured,timeBlock) VALUES (%s,%s,%s,%s,%s,%s,%s)",(temp_bmp,temp_bmp_f,pressure,altitude,currentDate,time_of_reading,block))

    print "Saved to BMP 180 Table"
    return "true"

def saveToDHT(temp_dht,temp_dht_f,humidity_dht):

    con=mdb.connect(Admin.MySQLCredentials.host, Admin.MySQLCredentials.user, Admin.MySQLCredentials.password, Admin.MySQLCredentials.database)

    with con:
        cur=con.cursor()
        cur.execute("INSERT INTO dht22 (reading_id,temperature_c,temperature_f,humidity,dateMeasured,hourMeasured,timeBlock) VALUES ((SELECT reading_id from bmp180 WHERE hourMeasured = %s),%s,%s,%s,%s,%s,%s)",(time_of_reading,temp_dht,temp_dht_f,humidity_dht,currentDate,time_of_reading,block))
    print "Saved to DHT 22 Table"
    return "true"


def writeData():

    saveToBMP(temp_bmp,temp_bmp_f,pressure,altitude)

    if humidity_dht is not None and temp_dht is not None:
        saveToDHT(temp_dht,temp_dht_f,humidity_dht)


def createTable():
    try:
        queryFile=file(sqlFile,"r")

        con=mdb.connect(Admin.MySQLCredentials.host, Admin.MySQLCredentials.user, Admin.MySQLCredentials.password, Admin.MySQLCredentials.database)
        currentDate=datetime.datetime.now().date()

        with con:
            line=queryFile.readline()
            query=""
            while(line!=""):
                query+=line
                line=queryFile.readline()

            cur=con.cursor()
            cur.execute(query)

    except IOError:
        pass #table has already been created



# Create the table and write the data to the database #####################
#createTable()
status=writeData() #get the readings

"""
# Log to the Google Sheet ####################################################
print 'Logging sensor measurements to {0}.'.format(Admin.GoogleSheetCredentials.name)
print 'Press Ctrl-C to quit.'
worksheet = None
run = True
attempt = 1
while run:
        # Login if necessary.
        if worksheet is None:
                worksheet = login_open_sheet(Admin.GoogleSheetCredentials.json, Admin.GoogleSheetCredentials.url)


        # Append the data in the spreadsheet, including a timestamp
        try:
                worksheet.insert_row((time_of_reading, temp_bmp_f, temp_bmp, pressure, altitude, temp_dht_f, temp_dht, humidity_dht), index=2)
                #worksheet.append_row((time_of_reading, temp_bmp_f, temp_bmp, pressure_bmp, altitude_bmp, temp_dht_f, temp_dht, humidity_dht))
                run = False
        except:
                # Error appending data, most likely because credentials are stale.
                # Null out the worksheet so a login is performed at the top of the loop.
                print 'Append error, logging in again'
                worksheet = None
                time.sleep(5)
                # Only try 5 times, then move on
                attempt = attempt + 1
                if attempt < 6:
                    continue
                else:
                    print "Failed to log to Google Sheet"
                    break

        print 'Wrote a row to {0}'.format(Admin.GoogleSheetCredentials.name)
        run = False
"""

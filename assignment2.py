import argparse
import urllib
import urllib.request
import ssl
import pypdf
from pypdf import PdfReader
import sqlite3
import os
import re
from datetime import datetime
import googlemaps
# this is used for the location rank and the incident rank
from collections import Counter
from math import sin, cos
from math import radians, degrees, sqrt
from math import asin, atan2

import openmeteo_requests

import requests_cache
import pandas as pd
import numpy as np
from retry_requests import retry
#without this I will receive the ssl error
ssl._create_default_https_context = ssl._create_stdlib_context



# this function is designed in order to accept the url from the 
# main function and fetch on incident pdf from the given url
def fetchincidents(url):
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"                          
    data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()  

    return data

# this function is responsible to extract take the data received from fetchincidents
# and write it in a pdf file and finally extract each row as a element of the list content1
def extractincidents(incident_data):
    # if i do 'w' instead of 'wb' there will be an error as incident_data isn't a str
    with open('incident.pdf','wb') as file1:
        file1.write(incident_data) 
    reader = PdfReader('incident.pdf')
    content = ''
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        content+=page.extract_text()
        content+='\n'
        content1 = list(content.split('\n'))
        # if (content1[-1].split()[-1]=='DEPARTMENT'):
        #     content1.pop() 
# the last two lines are reductant as one is the line that was being 
# obtained due to the \n that i has to add at the end of every page and the 
# other one is the timestamp value that was avilable in the norman pd document
    content1.pop(-1)
    content1.pop(-1)
    # print(content)
    return content1

#creating an SQLite database file named normanpd.db and a table 'incidents' to store the extracted data.
def createdb():    
    # connecting to the database
    db = sqlite3.connect('resources/normanpd.db')
    cursor = db.cursor()

    # creating a table "incidents" to store the data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
        )
    ''')
    # committing the changes 
    db.commit()
    os.remove('incident.pdf')
    # returning the connection in order to no connect again and again
    return db

def populatedb(db, incidents):
    cur = db.cursor()
    # SQL INORDER TO NOT REPEAT THE DATA IN THE TABLE, ANOTHER OPTION WOULD BE TO 
    # # DROP THE TABLE AFTER DOING THE COUNT
    # cur.execute('''DELETE FROM incidents''')
    # address will be of atleast 2 words
    till = 5
    exception_time = ''
    exception_in = ''
    for incident in incidents[0:]:  # [1:0] as i don't want the value that are date/time, nature and so on.
        if ('Location' in incident):
            continue
        if (incident == ''):
            continue
        data = incident.split()
        exception = 0
        # For the case where the Ramp location is going in the second line
        if "RAMP" in data[0]:
            exception = 1

        if '/' not in incident and exception == 0:
            continue
        
        if data[-1] == "DEPARTMENT":
            data.pop()
            data.pop()
            # print(data)
        
        date_time = data[0] + ' ' + data[1]
        incident_number = data[2]
        till = 5
        for i in range (4, len(data)):
            # using camel casing to differentiating between location and the nature
            if (re.match(r'^[A-Z][a-z]', data[i]) and len(data[i])>1) or (data[i] == '911' or data[i] == 'COP' or data[i]=='MVA') : 
                till = i
                break
        location = ' '.join(data[3:till])
        ori = data[-1]
        nature_incident = ' '.join(data[till:-1])


        # Exception case as the location data reaches to 2 sentences
        if "RAMP" in data[0]:
            date_time = exception_time 
            incident_number = exception_in
            A1 = data[0][4:]  
            A2 = ' '.join(data[1:-1])  # Extend the list with elements from data[1:-1]
            nature_incident = A1+' '+A2
            location = 'RAMP'
            ori= data[-1]
            # incident_type = ' '.join(incident_type_list)  # Join the elements with a space separator
        # # in the case when the nature field is empty
        # if (location == ori):
        #     nature_incident = 'empty'
        
        #DEBUGGING PRINT STATEMENT
        # print (f'dt:{date_time}, in:{incident_number}, loc:{location}, ni:{nature_incident}, ori:{ori}')
        #SQL COMMAND
        # Not allowing wrong data to enter the database.
        if 'RAMP' in nature_incident:
            exception_time = date_time
            exception_in = incident_number 
            continue
        cur.execute('''INSERT INTO incidents VALUES (?, ?, ?, ?, ?)''', (date_time, incident_number, location, nature_incident, ori))
    db.commit()

# printing incident nature counts sorted by frequency and alphabetically.
def status(db):
    # print('hi')
    cur = db.cursor()
    # SQL COMMAND
    cur.execute('''SELECT nature, COUNT(*) AS repeat FROM incidents GROUP BY nature ORDER BY repeat DESC, nature ASC''')
    # FINAL OUTPUT
    # output = '\n'.join(['|'.join(map(str, row)) for row in cur.fetchall()])
    alldata = cur.fetchall()
    datas=[]
    # print(alldata)
    for data in alldata:
        datas.append(data[1])
        # print('|'.join(map(str, data)))
        
    # CLOSING THE DATABASE AS THIS IS THE LAST PLACE WHERE IT WAS NEEDED
    return (datas)

# All this function does is take out the value that was pushed in the database during assignment0
def fetchdata(db): 
    cur = db.cursor()
    cur.execute("SELECT * from incidents")
    alldata = cur.fetchall()
    # this containes all the rows in the database, which are all the rows of all the files that are obtained by the 
    #urls in the files.csv
    return alldata

#This function returns the Day of the week and Time of the Day, by datetime. 
def DowTod(alldata):
    numericday =[]
    time = []
    for i in alldata:
        #using datetime to strip out the time and the date.
        incident_time = datetime.strptime(i[0], '%m/%d/%Y %H:%M')
        #appending the day of the week data
        #Sunday = 1, and Saturday = 7
        numericday.append(incident_time.isoweekday() % 7 + 1)
        #appending the time of the day data
        # 0 =12 am and 23 = 11 pm
        time.append(incident_time.hour)

    return numericday, time

#This function check if the incident ori is 'EMSSTAT' or is related to one with 'EMSSTAT' as incident ori 
def emssat(alldata):
    #putting all the values as False at the start.
    emssatVal = ['False'] * len(alldata)
    #making a set of all the true cases.
    trueCases = set()
    #initially checking for incident that have incident ori as 'EMSSTAT'
    for i in range(len(alldata)):
        if alldata[i][-1] == 'EMSSTAT':
            trueCases.add(i)
    # Using two for loops to check for other true cases (instances that are associated with incident with ori = 'EMSSTAT')
    for i in range(len(alldata)):
        point = alldata[i]
        #to check if the location and date is same as the one that is in a data with ori as "EMSSTAT"
        for j in range(len(alldata)):
            if j != i and point[0] == alldata[j][0] and point[2] == alldata[j][2] and alldata[j][-1] == 'EMSSTAT':
                trueCases.add(i)
    #Marking all those case as True
    for case in trueCases:
        emssatVal[case] = 'True' 
    return emssatVal

#this function is used to find the ranking based on the frequency of location. Using variables like current rank and 
# rank offset to find out the ranking in the manner mentioned in the instructions.
def locationRank(alldata):
    locationList = []
    locationRanks = {}
    currentRank = 1

    # seperation all the locations and creating a differnet list
    for i in alldata:
        locationList.append(i[2])
    
    # using counter to count all the location(finding frequency)
    locationCount = dict(Counter(locationList))
    # sorting the count
    locationCounted = sorted(locationCount.items(), key=lambda x: x[1], reverse=True)
    lastCount =0
    nextRank = 0
    # using the count to rank the locations
    for location, count in locationCounted:
        if count != lastCount:
            currentRank += nextRank
            nextRank = 0
        locationRanks[location] = currentRank
        nextRank += 1
        lastCount = count
    # print(locationRank)
    return locationRanks

#this function is used to find the ranking based on the frequency of incidents. Using variables like current rank and 
# rank offset to find out the ranking in the manner mentioned in the instructions. Same approach that was used in the location ranking.
def incidentRank(alldata):
    incidentList = []
    currentRank = 1
    # seperation all the incidents and creating a differnet list
    for i in alldata:
        incidentList.append(i[3])
    # using counter to count all the incidents(finding frequency)
    incidentCount = dict(Counter(incidentList))
    incidentCounted = sorted(incidentCount.items(), key=lambda x: x[1], reverse=True)
    incidentRanks ={}
    lastCount = 0
    nextRank = 0
    # using the count to rank the incident
    for incident, count in incidentCounted:
        if count != lastCount:
            currentRank += nextRank
            nextRank = 0
        incidentRanks[incident] = currentRank
        nextRank += 1
        lastCount = count
    # print(incidentRank)
    return incidentRanks

#this function used the location to find out the location's latitude and longitude and find the side of town 
def getSoT(alldata):
    #creating a google maps client using my key
    mapping = googlemaps.Client(key = 'AIzaSyAsOU_l0AyMgHkuI8v63OecfQ8yNLl5E7s')

    # locations = ['627 RANCHO DR', 'CLASSEN BLVD / E BROOKS ST', '24TH AVE SW / BEVERLY HILLS ST', '24TH AVE NW / W MAIN ST']
    locations = []
    # making a seperate list to store all the locations.
    for i in alldata:
        locations.append(i[2])

    SoT = {}
    latlong= {}
    # approximate center of the town for reference. 
    arproxcentLat = 35.220833
    approxcentLong = -97.443611
    # iterating for each location
    for location in locations:
        # adding ', Norman, OK' as without it i was getting multiple instances with no direction
        location1 = location + ', Norman, OK'
        #using the google api for each location
        callGeocode = mapping.geocode(location1)
        if not callGeocode:
            SoT[location]= 'No direction'
            continue 
        # getting the actual latitude and longitude of the location and storing it as it will be used
        # in finding the weather in that location in the time of the incident.  
        actualLat = callGeocode[0]["geometry"]["location"]["lat"]
        actualLong = callGeocode[0]["geometry"]["location"]["lng"]
        latlong[location] = [actualLat, actualLong]
        # The latitude and longitude are changed from degrees to radians
        firstLat, firstLong, secondLat, secondLong = map(radians, [arproxcentLat, approxcentLong, actualLat, actualLong])

        long = secondLong - firstLong

        #calculations for bearinig staring by calculating the X and Y components

        xComp = cos(secondLat) * sin(long)
        yComp = (cos(firstLat) * sin(secondLat)) - (sin(firstLat) * cos(secondLat) * cos(long))
        arctan = atan2(xComp, yComp)
        bearing = (degrees(arctan) + 360) % 360
        # list to define the directions
        dir = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        j = round(bearing/45)%8
        # gives the closes direction.
        dir = dir[j]

        #stores the dir of a location in the dic, location as key and the direction as value.
        SoT[location] = dir
    # print(SoT)
    # print(latlong)
    return latlong, SoT

# this function gets the weather code for a location at a particular time
def checkWeather(latlong, alldata, time):
    #creating a caching session to store and retrieve API responses, with no expiry and 
    # adding a retry mechanism on the cached session for reliability
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    # creating a client for the OpenMeteo API using the retry-enabled session
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # URL for the OpenMeteo API to fetch historical weather data
    url = "https://archive-api.open-meteo.com/v1/archive"
    date = []
    weather_code ={}

    # for i in alldata:
    #     start_date = i[0].split('')
    #     start_date = start_date[0].split('/')
    #     if len(start_date[0]) == 1:
    #         start_date[0] = '0'+start_date[0]
    #     if len(start_date[1]) == 1:
    #         start_date[1] = '0'+start_date[1]
    #     start_date = f'{start_date[2]}-{start_date[0]}-{start_date[1]}'
    #     date.append(start_date)

    for i in range(len(alldata)):
        hourly_data ={}
        # finding the date for which the weather is to be calculated.
        start_date1 = alldata[i][0]
        start_date = start_date1.split(' ')
        start_date = start_date[0].split('/')
        if len(start_date[0]) == 1:
            start_date[0] = '0'+start_date[0]
        if len(start_date[1]) == 1:
            start_date[1] = '0'+start_date[1]
        start_date = f'{start_date[2]}-{start_date[0]}-{start_date[1]}'  
        if (start_date, alldata[i][2]) not in weather_code.keys() and alldata[i][2] in latlong.keys(): 
            # print(latlong[alldata[i][2]][0])  
            # print(latlong[alldata[i][2]][1])       
            #defining the latitude, longitude, start_date and end_date(same as startdate as API call for a single day)
            params = {
                    "latitude": latlong[alldata[i][2]][0],
                    "longitude": latlong[alldata[i][2]][1],
                    "start_date": start_date,
                    "end_date": start_date,
                    "hourly": "weather_code"
                }
            # storing the response obtained
            responses = openmeteo.weather_api(url, params=params)
            # obtaining the response
            response = responses[0]
            #Taking out the hourly detail of the response
            hourly = response.Hourly()
            #getting the value needed
            hourly_weather_code = hourly.Variables(0).ValuesAsNumpy()
            hourly_data["weather_code"] = hourly_weather_code
            # storing the needed information based on the time the incident took place.
            weather_code[(start_date1, alldata[i][2])] = hourly_data["weather_code"][time[i]]

    # print(hourly_data)
    return weather_code

def main(urls):

    # print(url)
    # for fetching the data
    for url in urls:
        # for creating new database if it is not aviable
        
        incident_data = fetchincidents(url)
        # DEBUGGING PRINT STATEMENT
        # print(len(incident_data))

        # for extracting the  data
        incidents = extractincidents(incident_data)
        # DEBUGGING PRINT STATEMENT
        # print(len(incidents))
        db = createdb()

        # REMOVING THE FILE AS IT IS NOT IN THE SUBMISSION FORMAT
        # os.remove('incident.pdf')

        # inserting the data in the database
        populatedb(db, incidents)
	
    # # calculating and printing out the incident's nature counts
    status(db)
    #Assignment 2 work 
    #fetching all data
    alldata = fetchdata(db)
    #getting day of the week and the Time of the day
    numericday, time = DowTod(alldata)
    # print(alldata)
    # print(numericday)
    #getting the nature of the incident directly from the data
    nature = [data[3] for data in alldata]
    #getting the true false for each instance
    emmssatVal = emssat(alldata)
    # print(alldata)
    #getting a dict that contains location as key and ranking as value
    locationRanks = locationRank(alldata)

    # print(locationRanks)
    # print(len(locationRanks))
    #getting a dict that contains incident as key and ranking as value.
    incidentRanks = incidentRank(alldata)

    # getting the Latlong dict that contains the latitude longitude details of a location and SoT that containes the side of town details
    latlong, SoT = getSoT(alldata)
    # # latlong = {'24TH AVE NW / W MAIN ST': [35.2183478, -97.4766073], 'CLASSEN BLVD / E BROOKS ST': [35.2074806, -97.4341094], '24TH AVE SW / BEVERLY HILLS ST': [35.2006307, -97.47668329999999], '627 RANCHO DR': [35.216136, -97.42649569999999]}
    # getting a dict that contains location and time as the key and weather code as Value
    WeatherCode = checkWeather(latlong, alldata, time)


    print('Day of the Week\tTime of Day \t Weather \t Location Rank \t Side of town \t Incident Rank \t Nature \t EMMSTAT')
    for i in range(len(alldata)):

        print(f'{numericday[i]}\t{time[i]}\t{WeatherCode[(alldata[i][0],alldata[i][2])]}\t{locationRanks[alldata[i][2]]}\t{SoT[alldata[i][2]]}\t{incidentRanks[alldata[i][3]]}\t{nature[i]}\t{emmssatVal[i]}')
    cur = db.cursor()
    # # SQL INORDER TO NOT REPEAT THE DATA IN THE TABLE, ANOTHER OPTION WOULD BE TO 
    # # DROP THE TABLE AFTER DOING THE COUNT
    cur.execute('''DELETE FROM incidents''')
    db.commit()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", type=str, required=True, 
                         help="The file mentioned will contain all the urls will be used")
     
    args = parser.parse_args()
    links = []
    with open(args.urls,'r') as csvfile:
        for line in csvfile:
            links.append(line.strip())

        main(links)
        





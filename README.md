# cis6930sp24-assignment2

## Author:
Abhinav Aryal
abhinavaryal@ufl.edu

## Assignment Description:
This assignment involves building a Python function to extract incident data from the Norman, Oklahoma police department's PDF reports hosted on their website. The extracted data includes Date/Time, Incident Number, Location, Nature, and Incident ORI. The data is then stored in an SQLite database, and incident nature counts are printed. After the data is extracted we start the process of data augmentation while keeping fairness bias in mind.

During this assignment the expectations was to build on the work we had done on assigment 0 so that we would be able to extract data from an online source and format that data in order to use it as we want use the data to augment the data. Assignment 2 expands on this by adding to the extracted data, addressing bias and fairness in data processing, and getting the data ready for more examination in pipeline steps that follow.


### The things that we were expected to do were:
#### Work done in Assignment 0
- Download the incident data from a pdf file from norman pd website
- Extract the data, and classify them as per date/time, incident number, location, nature of the incident, incident ori.
- Creation of database to insert the extract database.
- Using SQL to print out the number of time each nature of incident took place.
#### New Work in Assignment 2
- Improve the data that was retrieved for Assignment 0 and get it ready for more analytical work.
- This improvement would result in creation of a new data set that will have the Day of the week in which the accident took place, The time of the day in which the accident look place, the weather code of the time in which the accident took place and the side of the town in which the accident took place.
- In addition to that, we were also expected to find out the frequency of locations and incident and rank them, Both of these can be found in the dataset printed in the terminal. 


## How to Install:
pipenv install .

## How to Run:

pipenv run python assignment2.py --urls files.csv

the files.csv contains a list of urls that we want to extract data from. 

## Functions:

## Functions Used for Assignment 0 as well.

### fetchincidents(url):

This function is designed in order to accept the url from the main function and fetch on incident pdf from the given url.

### extractincidents(incident_data):

This function is responsible to extract take the data received from fetchincidents and write it in a pdf file and finally extract each row as a element of the list content1.

### createdb():

Creates an SQLite database file named normanpd.db and a table 'incidents' to store the extracted data.

### populatedb(db, incidents):

Inserts incident data into the normanpd.db database. Here we delete the data in the database at the start of the process so that we do not run the same data again and again everytime we run the python code.

### status(db):

Prints incident nature counts sorted by frequency and alphabetically.

## New Functions created for assignment 2

### fetchdata(db):
This function is used to fetch the data from the data base that was stored in the previous assignment. 

### DowTod(alldata):
This function expects all the data fetch from fetchdata and uses the data to Day of the week and the time of the date. The function returns two list, one will contain the day of the week which will be from 1 to 7, here 1 will be sunday and 7 will be saturday. We can then use to list to find out the instance it relates to by the help of indexing as it is one to one mapping.

### emssat(alldata):
This fucntion also takes alldata as parameter and uses it to find all the instances that has EMSSAT as incident ori or has same location and time as the one that has incident ori as EMSSAT. This function will return a list that contains true or false for each row of the database and can be used later by the help of indexing as value in 0 index represents the first data in the database and so on. 

### locationRank(alldata):

This function is created in order to count the number of a times a incident has been reported in a particular location and rank them based on the frequency of the incidents in a particular location. The ranking is done in a manner that if there is a two way tie between two loctions for the most rank than both of them will be ranked as 1 and the subsequent location will be ranked as 3 as two are ranked as 1. This function returns a dict that containes the locations as the keys and the the rank for that location as the value fot that key.

### incidentRank(alldata):

This function is created in order to count the number of a times a incident has been reported and rank them based on the frequency of the incidents. The ranking is done in a manner that if there is a two way tie between two loctions for the most rank than both of them will be ranked as 1 and the subsequent incident will be ranked as 3 as two are ranked as 1. This function returns a dict that containes the incident as the keys and the the rank for that incident as the value fot that key.

### getSoT(alldata):

This function is created to find the side of the town the location lies on. This is done by finding the latitude and longitude of the location and comparing it to the appriximate center of the town (35.220833, -97.443611). I used the Google Maps API to geocode addresses and calculate their directional bearings from a central point in Norman, OK which is provided above. For each address, i made a change so that i can find all the latitude and longitude by adding ", Norman, OK" for precise geocoding. If even after that I am not able to find the side of the town, I pass it as 'no direction'. This funciton returns latlong that contains the latitude and longitude of each location and the SoT dict that contains the location as key and the Side of Town as the Value of the location. To avoid unnecessary API calls I created a set of all the locations to remove out any repeated locations so that I don't have to call the API for the same location twice.  

### checkweather(latlong, alldata, time):

Using the Open-Meteo API, I get historical weather data from a dataset keyed by location and date in this function. For efficiency and dependability, it starts an API session that is cached and has retry enabled. The function prepares the date, verifies the cache before querying, and then obtains hourly weather codes for each distinct date and location. Each pair of dates and locations has a corresponding code that is kept in a dictionary. Because of the setup's few API calls and gentle handling of any errors, the function is reliable for effectively retrieving and maintaining historical weather data. I use the latlong dict that I made in the previous SoT function to find the weather at that particular location. The function returns the weather code as the values and the location and time as the keys. For those cases that has the same location at the same time it will only call the API once which will avoid any unnecessary API calls. 

## Database Development:
The createdb() function creates an SQLite database file named normanpd.db in the resources/ directory. The table 'incidents' has the following schema:

db = sqlite3.connect('resources/normanpd.db')
The above is the code that helped us to connect our program to the sqlite database.

### The SQLite query used to create the data base:

    CREATE TABLE incidents (
        incident_time TEXT,
        incident_number TEXT,
        incident_location TEXT,
        nature TEXT,
        incident_ori TEXT
    );

### The SQLite query used to populate the database:

    INSERT INTO incidents VALUES (?, ?, ?, ?, ?)''', (date_time, incident_number, location, nature_incident, ori);

### The SQLite query used to delete the data in the database before re-running the populatedb process:

    DELETE FROM incidents;

### The SQLite query used to check the status of each nature of incident:

    SELECT nature, COUNT(*) AS repeat 
    FROM incidents 
    GROUP BY nature 
    ORDER BY repeat DESC, nature ASC;

### The SQLite query used fetch all the data from the database:
    SELECT * from incidents


## DATASHEET.md

The dataset that comes after the data augmentation was  developed by Abhinav Aryal for a Data Engineering class at the University of Florida, this dat set enhances police incident records from Norman PD by incorporating additional data fields such as weather conditions and side of town information for a particular incident. This dataset was created to made in order to have a way to deeply analyse the Norman PD incidents dataset, helping to identify patterns and correlations that were not as evident in the original data.
An overview of the datasheet is:

Motivation: To augment police incident data for improved analytical insights.
Composition: Includes fields like day, time, weather, location and incident ranks, and EMS status, aligning with the original dataset count.
Collection and Augmentation: Utilizes Google Maps and historical weather APIs to enrich location and weather details.
Use Cases: Suitable for academic research, crime analysis, and urban studies. It should not be used for direct operational policing to avoid biases.
Maintenance: Maintained by the creator, updates available via GitHub. For contributions or queries, contact Abhinav Aryal at abhinavaryal@ufl.edu.

## OUTPUT
The output obtain from this program can be viewed in the terminal, as it is printed. For each url in the files.csv we give the datset that contains Day of the Week, Time of Day, Weather, Location Rank, Side of Town, Incident Rank, Nature and EMSSTAT, all this are tab separated rows. No more beautification has been done in the way the output is printed as it may affect the way the output is tested in the autograder than what has been mentioned in the assignment instructions.

## LICENSE
Added MIT License to the project.

## Bugs and Assumptions:
Addressing multiline cells with information: The code assumes that some cells may contain information on multiple lines and handles such cases.

The cases that i came through where when the location details were exceeding one line, the pypdf reader would consider them as different data so I had difficulty with handling this kind of data, so for that I created exception cases for those and didn't allow those wrong data to enter the database and checked for the following data to obtain the nature and the ori, at the end this issue was fixed but a better solution can be found.
An assumption that I have made is that each letter in the Location will always be in CAPTIAL LETTERS. An assumptin was also made that if the geocoder give me N as the side of town and the Location has NE then we will print out the output obtained from geocoder as the maths for this can be a little complex. 

This project is highly depended on the API calls for the side of town (Google map API) and the Weather Code (Historical weather API) so if any thing trigger a breakdown to the API call then the program can face a problem. 
If the latitude and longitude is not calculated by the google maps API then finding the weather code is not possible.

The Google Map API is a billable API so many test cases were not ran on this assignment to fit under the Credit obtained from Google and Dr. Grant at the start of semester and so that there are enough credit remaining so that the credits can be used during the checking process of the assignment. Humble request to not use the API on huge amount of data as it may end up crossing the credit available and become chargeable.

## Test:

In my tests files six files can be found, Each file checks multiple functionality of the code. The first test file test_download is associated with assignment0, but as downloading the data from Norman PD is important, I decided to keep the testing for that function here, to ensure that the data is reaching the database correctly.

There are other test cases that are related to the assignment 2 and they do :

- test_DoWToD: 
This pytest checks two things:
    - If the Day of the week obtained from the function is same as the Day mentioned in the data from norman PD
    - If the Time of the day is same as the one obtained from the Function.
- test_EMSSATAT: 
This pytest checks:
    - If the instance that doesn't have 'EMSSTAT' as the incident ori but has the same location and time as the one that has 'EMSSTAT' give me true in return. 
- test_RankingFunctions:
This pytest checks:
    - If the manner in which both incident ranking and location ranking takes place in the manner that has been mentioned in the way we have been told to do in the instructions.
- test_SoT: 
This pytest checks:
    - If the Side of Town coming matches the side of Town value of not.
    - If the latitude and longitude obtained is same as the latitude and longitude of the location. This is important as we use the latitude and longitude in the weather fucntion as well.
- test_WeatherCode:
This pytest checks:
    - If the Weather code obtained from the function is the same as the weather Code of that day.


The pytest can be ran by using the shell code:
    pipenv run python -m pytest   
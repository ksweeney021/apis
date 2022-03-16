import sys
# import pandas as pd
# thought I needed pandas originally based on first googles for exporting python to csv
import json
import requests
import csv

# grabbed some of the active fires in cali from the list and attempted to get to the data I needed with this hardcoded first
# Simulation of return values from the calls
# calls = [
#     {
#         "AcresBurned": None,
#         "AdminUnit": "Cleveland National Forest ",
#         "AdminUnitUrl": None,
#         "AgencyNames": "",
#         "CalFireIncident": False,
#         "ControlStatement": None,
#         "County": "Orange",
#         "ExtinguishedDate": "",
#         "ExtinguishedDateOnly": "",
#         "Final": false,
#         "IsActive": true,
#         "Latitude": 33.67691,
#         "Location": "Holy Jim Canyon & Trabuco Creek Road, northeast of Rancho Santa Margarita",
#         "Longitude": -117.5181037,
#         "Name": "Jim Fire ",
#         "NotificationDesired": false,
#         "PercentContained": None,
#         "Started": "2022-03-02T11:06:00Z",
#         "StartedDateOnly": "2022-03-02",
#         "Type": "Wildfire",
#         "UniqueId": "e4391d31-46b5-49ad-b4d5-4a934b73d08b",
#         "Updated": "2022-03-04T19:38:14Z",
#         "Url": "https://www.fire.ca.gov/incidents/2022/3/2/jim-fire/"
#     },
#     {
#         "AcresBurned": 88.0,
#         "AdminUnit": "CAL FIRE Shasta-Trinity Unit ",
#         "AdminUnitUrl": None,
#         "AgencyNames": "",
#         "CalFireIncident": true,
#         "ControlStatement": None,
#         "County": "Shasta",
#         "ExtinguishedDate": "",
#         "ExtinguishedDateOnly": "",
#         "Final": false,
#         "IsActive": true,
#         "Latitude": 40.67671,
#         "Location": "Flanagan Road and N Beltline Road, west of Shasta Lake City",
#         "Longitude": -122.4073,
#         "Name": "Flanagan Fire ",
#         "NotificationDesired": false,
#         "PercentContained": 90.0,
#         "Started": "2022-03-04T10:31:00Z",
#         "StartedDateOnly": "2022-03-04",
#         "Type": "Wildfire",
#         "UniqueId": "719127a0-5d9b-42e6-985f-ce3e6a718c0e",
#         "Updated": "2022-03-07T19:00:57Z",
#         "Url": "https://www.fire.ca.gov/incidents/2022/3/4/flanagan-fire/"
#     }
# ]

# url to get active fires in cali
url = 'https://www.fire.ca.gov/umbraco/api/IncidentApi/List'
# request to get active fires in cali
r = requests.get(url)
# parse json
output = r.json()

# url to get earthquakes within 1000km of active fires in cali
countUrl = 'https://earthquake.usgs.gov/fdsnws/event/1/count'
# params = {'format': 'xml', 'eventtype': 'earthquake', 'latitude': '33.67691', 'longitude': '-117.5181037', 'maxradiuskm': '1000', 'orderby': 'time-asc', 'includeallmagnitudes': 'true'}
# gridUrl = 'https://api.weather.gov/points/40.6767,-122.4073'
# elevationUrl = 'https://api.weather.gov/gridpoints/STO/27,167'

# loop through active fire list & grab all lat/longs
result = []
for obj in output:
    # print(obj['Latitude'])
    # print(obj['Longitude'])
    # set lat and long as variables for elevation api call
    latitude = str(obj['Latitude'])
    longitude = str(obj['Longitude'])
    # params for counting earthquakes within 1000km api call
    params = {'format': 'geojson', 'eventtype': 'earthquake', 'latitude': obj['Latitude'], 'longitude': obj['Longitude'], 'maxradiuskm': '1000', 'orderby': 'time-asc'}
    # get earthquakes within 1000km api call
    r2 = requests.get(countUrl, params=params)
    countOutput = r2.json()
    # set variable for earthquakes from previous api call
    earthquakes = str(countOutput['count'])
    # print(countOutput) --> testing throughout process
    # setting URL to find grid points for lat/longs elevation
    pointUrl = 'https://api.weather.gov/points/' + latitude + ',' + longitude
    # api call for lat/long to get elevation
    r3 = requests.get(pointUrl)
    pointsOutput = r3.json()
    # get variables for next api call for gridpoints API call
    gridId = str(pointsOutput['properties']['gridId'])
    gridX = str(pointsOutput['properties']['gridX'])
    gridY = str(pointsOutput['properties']['gridY'])
    # print(gridUrl) --> more testing
    # api call for getting elevation
    elevationUrl = 'https://api.weather.gov/gridpoints/' + gridId + '/' + gridX + ',' + gridY
    # final api call
    r4 = requests.get(elevationUrl)
    # set output to json
    elevationOutput = r4.json()
    altitude = str(elevationOutput['properties']['elevation']['value'])

    # print(latitude), --> all testing
    # print(longitude),
    # print(earthquakes),
    # print(altitude)
    # fireRow = latitude + ',' + longitude + ',' + earthquakes + ',' + altitude
    fireRows = [latitude,longitude,earthquakes,altitude]

    # set results from looping through as an array to output to csv later
    result.append(fireRows)
# print(result)

# output to csv
header = ['latitude', 'longitude', '# of earthquakes in 1000km', 'elevation in m']

# open file to write to
with open('/Users/kellysweeney/miniconda3/backstop.csv', 'w') as csv_file:
    # create the csv writer to my file using writer function from csv module
    writer = csv.writer(csv_file)
    # write to csv
    writer.writerow(header)
    writer.writerows(result)

    # print(elevationUrl) --> testing

#print(output) --> testing

# beginning attempt for csv using pandas, which I discovered I did not need later on
# Create an initial empty data frame
# df = pd.DataFrame()
# # Make the consecutive calls
# for i, call in enumerate(output):
#     # Create the new DataFrame from the data you got
#     df_new = pd.DataFrame(call).set_index('Latitude')
#     # Rebane the column to avoid collision
#     df_new.rename(columns={'Longitude': 'Longitude_%s' % i}, inplace=True)
#     # Merge it with the current data frame
#     df = pd.concat([df, df_new], axis=1)
# # Save data to file (I'm using here the sys.stdout, just
# # to print it to console.
# df.to_csv(sys.stdout, header=None)

exit()

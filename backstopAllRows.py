import json
import requests
import csv

# get active fires in cali
url = 'https://www.fire.ca.gov/umbraco/api/IncidentApi/List'
r = requests.get(url)
output = r.json()

# get earthquakes within 1000km of active fires in cali
countUrl = 'https://earthquake.usgs.gov/fdsnws/event/1/count'

result = []
for obj in output:
    latitude = str(obj['Latitude'])
    longitude = str(obj['Longitude'])
    params = {'format': 'geojson', 'eventtype': 'earthquake', 'latitude': obj['Latitude'], 'longitude': obj['Longitude'], 'maxradiuskm': '1000', 'orderby': 'time-asc'}
    # get earthquakes within 1000km api call
    r2 = requests.get(countUrl, params=params)
    countOutput = r2.json()
    earthquakes = str(countOutput['count'])
    # get grid points to later find elevation
    pointUrl = 'https://api.weather.gov/points/' + latitude + ',' + longitude
    # api call for lat/long to get elevation
    r3 = requests.get(pointUrl)
    pointsOutput = r3.json()
    gridId = str(pointsOutput['properties']['gridId'])
    gridX = str(pointsOutput['properties']['gridX'])
    gridY = str(pointsOutput['properties']['gridY'])
    # get lat/long's elevation - final api call
    elevationUrl = 'https://api.weather.gov/gridpoints/' + gridId + '/' + gridX + ',' + gridY
    r4 = requests.get(elevationUrl)
    elevationOutput = r4.json()
    altitude = str(elevationOutput['properties']['elevation']['value'])

    fireRows = [latitude,longitude,earthquakes,altitude]
    # set results from looping through as an array to output to csv later
    result.append(fireRows)

# output to csv
header = ['latitude', 'longitude', '# of earthquakes in 1000km', 'elevation in m']

with open('/Users/kellysweeney/apis/backstopAllRows.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(header)
    writer.writerows(result)

exit()

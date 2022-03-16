# figuring out this is all I need in order to hit all the API's
import json
import requests

url = 'https://www.fire.ca.gov/umbraco/api/IncidentApi/List'

r = requests.get(url)

output = r.json()

print(output)

exit()


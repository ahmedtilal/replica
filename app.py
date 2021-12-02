import singer
import urllib.request
import json
#Here is a dummy JSON Schema for the sample data passed by our REST API.
schema = {'properties': {
'id': {'type': 'string'},
'employee_name': {'type': 'string'},
'employee_salary': {'type': 'string'},
'employee_age': {'type': 'string'},
'profile_image': {'type': 'string'}}}

#Here we make the HTTP request and parse the response
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
req = urllib.request.Request(url= 'http://dummy.restapiexample.com/api/v1/employees', headers = headers)
with urllib.request.urlopen(req) as response:
    emp_data = json.loads(response.read().decode('utf-8'))
#next we call singer.write_schema which writes the schema of the employees stream
singer.write_schema('employees', schema, 'id')
#then we call singer.write_records to write the records to that stream
singer.write_records('employees', records=emp_data["data"])
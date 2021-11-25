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
with urllib.request.urlopen('http://dummy.restapiexample.com/api/v1/employees') as response:
    emp_data = json.loads(response.read().decode('utf-8'))
#next we call singer.write_schema which writes the schema of the employees stream
singer.write_schema('employees', schema, 'id')
#then we call singer.write_records to write the records to that stream
singer.write_records('employees', records=emp_data["data"])
import requests
import json
api_swagger = requests.get('https://api.data.world/v0/swagger.json').text
api_swagger = api_swagger.encode('ascii', 'ignore').decode('ascii')
api_swagger = json.loads(api_swagger) 
with open('datadotworld/client/swagger-dwapi-def.json') as f:
    python_swagger = f.read()
python_swagger = python_swagger.encode('ascii', 'ignore').decode('ascii')
python_swagger = json.loads(python_swagger) 
print set(api_swagger['paths'].keys()) - set(python_swagger['paths'].keys())
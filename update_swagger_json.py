import requests
import json
api_swagger = requests.get('https://api.data.world/v0/swagger.json').text
api_swagger = api_swagger.encode('ascii', 'ignore').decode('ascii')
api_swagger = json.loads(api_swagger)
with open('datadotworld/client/swagger-dwapi-def.json', 'w') as f:
    f.write(json.dumps(api_swagger, indent=4, sort_keys=True))

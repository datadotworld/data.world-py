import datadotworld as dw

api_client = dw.api_client()

test = api_client.get_insights_for_project('patrickzhang/python', limit = 1)
print(test)
data = {
  "title": "My insight",
  "description": "This is an example of an insight.",
  "body": {
    "imageUrl": "https://example.com/image.png"
  },
  "sourceLink": "https://example.com/dashboard",
  "dataSourceLinks": [
    "https://data.world/jonloyens/intermediate-data-world/workspace/query?queryid=23e7f574-3020-4683-bc89-123e12cf039e"
  ]
}
api_client.create_insight('patrickzhang/python', title)

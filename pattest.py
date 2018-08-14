import datadotworld as dw

api_client = dw.api_client()

test = api_client.get_insights_for_project('patrickzhang/python', limit = 1)
body = {
    "markdownBody": "hello"
  }
test2 = api_client.get_insight('patrickzhang/python', 'ef291df4-c884-49df-980d-cb01b24a719c')

api_client.replace_insight('patrickzhang/python', 'ef291df4-c884-49df-980d-cb01b24a719c', title='replaced insight', description='replaced', body=body)

# api_client.create_insight('patrickzhang/python', title='created new', description='changed', body=body)

# api_client.update_insight('patrickzhang/python', 'afd504ba-f709-4960-87a6-69a9cf27e10d', 
# 	title='updated new', description='updated')

# api_client.delete_insight('patrickzhang/python', '732246c0-8bdb-4903-846d-c87b1e231a37')
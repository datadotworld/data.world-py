import datadotworld as dw

api_client = dw.api_client()

#------------------------------
# Projects

api_client.projects.create_project('patrickzhang', title="myproject", visibility="OPEN")

api_client.projects.get_project('patrickzhang', 'myproject')

api_client.projects.patch_project('patrickzhang', 'myproject', title="chjjjjjit")

api_client.projects.replace_project('patrickzhang', 'myproject', title="replaced", visibility="OPEN")

api_client.projects.delete_project('patrickzhang', 'myproject')

api_client.projects.add_linked_dataset('patrickzhang', 'python', 'patrickzhang', 'testing2')

api_client.projects.remove_linked_dataset('patrickzhang', 'python', 'patrickzhang', 'testing2')

# ------------------------------
# Datasets

api_client.datasets.create_dataset('patrickzhang', title="mydataset", visibility="OPEN")

api_client.datasets.get_dataset('patrickzhang', 'mydataset')

api_client.datasets.patch_dataset('patrickzhang', 'mydataset', title="chjjjjjit")

api_client.datasets.replace_dataset('patrickzhang', 'mydataset', title="replaced", visibility="OPEN")

api_client.datasets.delete_dataset('patrickzhang', 'mydataset')


# ------------------------------
# Insights

api_client.insights.get_insights_for_project('patrickzhang', 'python', limit = 1)

body = {
    "markdownBody": "hello"
  }

test2 = api_client.insights.get_insight('patrickzhang', 'python', 'ef291df4-c884-49df-980d-cb01b24a719c')

api_client.insights.replace_insight('patrickzhang', 'python', title='replaced insight', description='replaced', body=body)

api_client.insights.create_insight('patrickzhang', 'python', title='created new', description='changed', body=body)

api_client.insights.update_insight('patrickzhang', 'python', 'afd504ba-f709-4960-87a6-69a9cf27e10d',
                          title='updated new looool', description='updated')

api_client.insights.delete_insight('patrickzhang', 'python', '732246c0-8bdb-4903-846d-c87b1e231a37')


# ------------------------------
# Users

test = api_client.users.get_user_data()
print(test.text)

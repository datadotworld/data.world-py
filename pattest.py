import datadotworld as dw

api_client = dw.api_client()
intro_project = api_client.get_project('patrickzhang/' 'project')
print(intro_project)

api_client.create_project('patrickzhang', title="Myol Project", visibility="OPEN")

api_client.update_project('patrickzhang', "myol-project", title="changed it")

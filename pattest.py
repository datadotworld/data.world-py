import datadotworld as dw

api_client = dw.api_client()

api_client.create_project('patrickzhang', title="project", visibility="OPEN")

intro_project = api_client.get_project('patrickzhang/project')

api_client.update_project('patrickzhang/project', title="changed it")
api_client.replace_project('patrickzhang/project', title="replaced", visibility="OPEN")

api_client.delete_project('patrickzhang/' 'project')

api_client.remove_linked_dataset('patrickzhang/python', 'patrickzhang/asd')

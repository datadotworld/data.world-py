import datadotworld as dw

api_client = dw.api_client()

api_client.projects.create_project('patrickzhang', title="myproject", visibility="OPEN")

api_client.projects.get_project('patrickzhang', 'myproject')

api_client.projects.patch_project('patrickzhang', 'myproject', title="chjjjjjit")

api_client.projects.replace_project('patrickzhang', 'myproject', title="replaced", visibility="OPEN")

api_client.projects.delete_project('patrickzhang', 'myproject')

api_client.projects.add_linked_dataset('patrickzhang', 'python', 'patrickzhang', 'testing2')

api_client.projects.remove_linked_dataset('patrickzhang', 'python', 'patrickzhang', 'testing2')
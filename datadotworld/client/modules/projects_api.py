import requests
from .api_client import ApiClient
import json

class ProjectsApi(object):
	def __init__(self, api_client=None):
		if api_client:
			self.api_client = api_client
		else:
			if not config.api_client:
				config.api_client = ApiClient()
			self.api_client = config.api_client
	# def get_project(self, owner, id, **kwargs):
	# 	r = requests.get('https://api.data.world/v0/datasets/{}/{}'.format(owner, id))


	def get_project(self, owner_id, project_id):
		url = '{}/projects/{}/{}'.format(self.api_client._api_url, owner_id, project_id)
		r = requests.get(url, headers=self.api_client.default_headers)
		return r.text

	def create_project(self, owner_id, **kwargs):
		#kwargs is Body of https://apidocs.data.world/api/projects/createproject
		try:
			url = '{}/projects/{}'.format(self.api_client._api_url, owner_id)
			#payload = {"title": kwargs.get('title', "My Project"), "visibility": kwargs.get('visibility', "PRIVATE")}
			r = requests.post(url, headers=self.api_client.default_headers, data=json.dumps(kwargs))
		except RequestException as e:
			raise e

	def update_project(self, owner_id, project_id, **kwargs): 
		#kwargs is Body of https://apidocs.data.world/api/projects/patchproject
		try:
			url = '{}/projects/{}/{}'.format(self.api_client._api_url, owner_id, project_id)
			r = requests.patch(url, headers=self.api_client.default_headers, data=json.dumps(kwargs))
			print(r.text)
		except RequestException as e:
			raise e


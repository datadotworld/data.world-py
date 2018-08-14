import requests
from requests.exceptions import RequestException
from .api_client import ApiClient
import json

class InsightsApi(object):
	def __init__(self, api_client=None):
		if api_client:
			self.api_client = api_client
		else:
			if not config.api_client:
				config.api_client = ApiClient()
			self.api_client = config.api_client

	def get_insight(self, owner_id, project_id, insight_id, **kwargs):
		url = '{}/insights/{}/{}/{}'.format(self.api_client._api_url, owner_id, project_id, insight_id)
		r = requests.get(url, headers=self.api_client.default_headers, params=kwargs)
		return r.text

	def get_insights_for_project(self, owner_id, project_id, **kwargs):
		'''List insights associated with a project.
		:param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param project_id: Unique identifier of project
        :type dataset_id: str
        :kwargs is Query of https://apidocs.data.world/api/insights/getinsightsforproject
        :limit: Maximum number of lines of items to include in a page of results
        :type limit: str
        :next: Token from previous result page to be used when requesting a subsequence page
        :type next: str
        '''
		url = '{}/insights/{}/{}'.format(self.api_client._api_url, owner_id, project_id)
		r = requests.get(url, headers=self.api_client.default_headers, params=kwargs)
		return r.text

	def create_insight(self, owner_id, project_id, **kwargs):
		'''Create a new insight.
		:param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param project_id: Project unique identifier
        :type project_id: str
        :kwargs is Body of https://apidocs.data.world/api/insights/createinsight
        '''
		try:
			url = '{}/insights/{}/{}'.format(self.api_client._api_url, owner_id, project_id)
			#payload = {"title": kwargs.get('title', "My Project"), "visibility": kwargs.get('visibility', "PRIVATE")}
			r = requests.post(url, headers=self.api_client.default_headers, data=json.dumps(kwargs))
		except RequestException as e:
			raise e

	def replace_insight(self, owner_id, dataset_id, insight_id, **kwargs):
		'''Create or replace a project with a given id. If a project exists with the same id, this call will reset such project redefining all its attributes.
		:param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param dataset_id: Unique identifier of dataset
        :type dataset_id: str
        :kwargs is Body of https://apidocs.data.world/api/projects/replaceproject
        '''
		url = '{}/insights/{}/{}/{}'.format(self.api_client._api_url, owner_id, dataset_id, insight_id)
		r = requests.put(url, headers=self.api_client.default_headers, data=json.dumps(kwargs))
		print(r.text)

	def update_insight(self, owner_id, dataset_id, insight_id, **kwargs):
		'''Update an existing insight. Only elements included in the request will be updated. All omitted elements will remain untouched.
		:param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param dataset_id: Unique identifier of dataset
        :type dataset_id: str
        :kwargs is Body of https://apidocs.data.world/api/projects/patchdataset
        '''
		try:
			url = '{}/insights/{}/{}/{}'.format(self.api_client._api_url, owner_id, dataset_id, insight_id)
			r = requests.patch(url, headers=self.api_client.default_headers, data=json.dumps(kwargs))
		except RequestException as e:
			raise e

	def delete_insight(self, owner_id, project_id, insight_id):
		'''Delete a project and associated data. This operation cannot be undone, but you may recreate the project using the same id.
		:User must have admin auth token
		:param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param dataset_id: Unique identifier of dataset
        :type dataset_id: str
        '''
		try:
			url = '{}/insights/{}/{}/{}'.format(self.api_client._api_url, owner_id, project_id, insight_id)
			r = requests.delete(url, headers=self.api_client.default_headers)
			print(r.text)
		except RequestException as e:
			raise e









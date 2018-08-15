import requests
from requests.exceptions import RequestException
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

	def get_project(self, owner_id, project_id):
		'''Retrieve a project. The definition of the project will be returned, not the associated data.
		:param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param project_id: Unique identifier of dataset
        :type dataset: str
        '''
		url = '{}/projects/{}/{}'.format(self.api_client._api_url, owner_id, project_id)
		r = requests.get(url, headers=self.api_client.default_headers)

	def create_project(self, owner_id, **kwargs):
		'''Create a new project.
		:param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :kwargs is Body of https://apidocs.data.world/api/projects/createproject
        '''
		try:
			url = '{}/projects/{}'.format(self.api_client._api_url, owner_id)
			#payload = {"title": kwargs.get('title', "My Project"), "visibility": kwargs.get('visibility', "PRIVATE")}
			r = requests.post(url, headers=self.api_client.default_headers, data=json.dumps(kwargs))
		except RequestException as e:
			raise e

	def patch_project(self, owner_id, project_id, **kwargs):
		'''Update an existing project. Only elements included in the request will be updated. All omitted elements will remain untouched.
		:param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param project_id: Unique identifier of dataset
        :type dataset: str
        :kwargs is Body of https://apidocs.data.world/api/projects/patchproject
        '''
		try:
			url = '{}/projects/{}/{}'.format(self.api_client._api_url, owner_id, project_id)
			r = requests.patch(url, headers=self.api_client.default_headers, data=json.dumps(kwargs))
		except RequestException as e:
			raise e

	def replace_project(self, owner_id, project_id, **kwargs):
		'''Create or replace a project with a given id. If a project exists with the same id, this call will reset such project redefining all its attributes.
		:param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param project_id: Unique identifier of dataset
        :type dataset: str
        :kwargs is Body of https://apidocs.data.world/api/projects/replaceproject
        '''
		url = '{}/projects/{}/{}'.format(self.api_client._api_url, owner_id, project_id)
		r = requests.put(url, headers=self.api_client.default_headers, data=json.dumps(kwargs))
		print(r.text)


	def delete_project(self, owner_id, project_id):
		'''Delete a project and associated data. This operation cannot be undone, but you may recreate the project using the same id.
		:User must have admin auth token
		:param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param project_id: Unique identifier of dataset
        :type dataset: str
        '''
		try:
			url = '{}/projects/{}/{}'.format(self.api_client._api_url, owner_id, project_id)
			r = requests.delete(url, headers=self.api_client.default_headers)
		except RequestException as e:
			raise e

	def add_linked_dataset(self, owner_id, project_id, linked_dataset_owner, linked_dataset_id, **kwargs):
		"""
		Link dataset
        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str owner: User name and unique identifier of the creator of a project. For example, in the URL: [https://data.world/government/how-to-add-depth-to-your-data-with-the-us-census-acs](https://data.world/government/how-to-add-depth-to-your-data-with-the-us-census-acs), government is the unique identifier of the owner. (required)
        :param str id: Project unique identifier. For example, in the URL:[https://data.world/government/how-to-add-depth-to-your-data-with-the-us-census-acs](https://data.world/government/how-to-add-depth-to-your-data-with-the-us-census-acs), how-to-add-depth-to-your-data-with-the-us-census-acs is the unique identifier of the project. (required)
        :param str linked_dataset_owner: (required)
        :param str linked_dataset_id: (required)
        :return: SuccessMessage
                 If the method is called asynchronously,
                 returns the request thread.
        """
		try:
			url = '{}/projects/{}/{}/linkedDatasets/{}/{}'.format(self.api_client._api_url, owner_id, project_id, linked_dataset_owner, linked_dataset_id)
			r = requests.put(url, headers=self.api_client.default_headers)
			return r.text
		except RequestException as e:
			raise e

	def remove_linked_dataset(self, owner_id, project_id, linked_dataset_owner, linked_dataset_id, **kwargs):
		try:
			url = '{}/projects/{}/{}/linkedDatasets/{}/{}'.format(self.api_client._api_url, owner_id, project_id, linked_dataset_owner, linked_dataset_id)
			r = requests.delete(url, headers=self.api_client.default_headers)
			return r.text
		except RequestException as e:
			raise e










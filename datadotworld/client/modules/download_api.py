import requests
from requests.exceptions import RequestException
from .api_client import ApiClient
import json
import zipfile, io
import re

class DownloadApi(object):
	def __init__(self, api_client=None):
		if api_client:
			self.api_client = api_client
		else:
			if not config.api_client:
				config.api_client = ApiClient()
			self.api_client = config.api_client

	def download_dataset(self, owner_id, dataset_id):
		'''
		Download a .zip file containing all files within a dataset as originally uploaded.
		:param owner_id: Username and unique identifier of creator of dataset or project
		:typeof owner_id: string
		:param dataset_id: Dataset unique identifier 
		:typeof dataset_id: string
		'''
		url = '{}/download/{}/{}'.format(self.api_client._api_url, owner_id, dataset_id)
		custom_headers = {
            'Authorization': 'Bearer {}'.format(self.api_client._api_token),
            'Content-Type': 'application/zip',
            'User-Agent': 'data.world-py'
        }
		r = requests.get(url, headers=custom_headers)
		z = zipfile.ZipFile(io.BytesIO(r.content))
		z.extractall()

	def download_file(self, owner_id, dataset_id, file):
		'''
		Download a file within the dataset as originally uploaded.
		:param owner_id: Username and unique identifier of creator of dataset or project
		:typeof owner_id: string
		:param dataset_id: Dataset unique identifier 
		:typeof dataset_id: string
		:param file: File name
		:typeof file: string
		'''
		url = '{}/file_download/{}/{}/{}'.format(self.api_client._api_url, owner_id, dataset_id, file)
		custom_headers = {
            'Authorization': 'Bearer {}'.format(self.api_client._api_token),
            'User-Agent': 'data.world-py'
        }
		r = requests.get(url, headers=custom_headers)
		print(r.headers['Content-Disposition'])
		filename = re.findall(r'"(.*?)"', r.headers['Content-Disposition'])[0]
		with open(filename, 'wb') as f:
			f.write(r.content)	










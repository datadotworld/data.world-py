import requests
from requests.exceptions import RequestException
import json
from datadotworld.util import parse_dataset_key
from uplink import Consumer, get, post, patch, put, delete, Header, Path, Body, json

class ProjectsApi(Consumer):
    @get("{owner_id}/{project_id}")
    def get_project(self, owner_id, project_id):
        '''Retrieve a project. The definition of the project will be returned, not the associated data.
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param project_id: Unique identifier of dataset
        :type dataset: str
        '''

    @json
    @post("{owner_id}")
    def create_project(self, owner_id, **kwargs: Body):
        '''Create a new project.
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :kwargs is Body of https://apidocs.data.world/api/projects/createproject
        '''

    @json
    @patch("{owner_id}/{project_id}")
    def patch_project(self, owner_id, project_id, **kwargs: Body):
        '''Update an existing project. Only elements included in the request will be updated. All omitted elements will remain untouched.
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param project_id: Unique identifier of dataset
        :type dataset: str
        :kwargs is Body of https://apidocs.data.world/api/projects/patchproject
        '''

    @json
    @put("{owner_id}/{project_id}")
    def replace_project(self, owner_id, project_id, **kwargs: Body):
        '''Create or replace a project with a given id. If a project exists with the same id, this call will reset such project redefining all its attributes.
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param project_id: Unique identifier of dataset
        :type dataset: str
        :kwargs is Body of https://apidocs.data.world/api/projects/replaceproject
        '''

    @delete("{owner_id}/{project_id}")
    def delete_project(self, owner_id, project_id):
        '''Delete a project and associated data. This operation cannot be undone, but you may recreate the project using the same id.
        :User must have admin auth token
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param project_id: Unique identifier of dataset
        :type dataset: str
        '''

    @json
    @put("{owner_id}/{project_id}/linkedDatasets/{linked_dataset_owner}/{linked_dataset_id}")
    def add_linked_dataset(self, owner_id, project_id, linked_dataset_owner, linked_dataset_id, **kwargs: Body):
        """
        Add Link dataset -> https://apidocs.data.world/api/projects/addlinkeddataset
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
    @json
    @delete("{owner_id}/{project_id}/linkedDatasets/{linked_dataset_owner}/{linked_dataset_id}")
    def remove_linked_dataset(self, owner_id, project_id, linked_dataset_owner, linked_dataset_id, **kwargs: Body):
        """
        Remove Link dataset -> https://apidocs.data.world/api/projects/removelinkeddataset
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

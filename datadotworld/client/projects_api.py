from uplink import Consumer, get, post, patch, put, delete, Body, json, args, Path


class ProjectsApi(Consumer):
    @get("projects/{owner_id}/{project_id}")
    def get_project(self, owner_id, project_id):
        """Retrieve a project.
        The definition of the project will be returned,
        not the associated data.
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param project_id: Unique identifier of dataset
        """

    @args(Path, Body)
    @json
    @post("projects/{owner_id}")
    def create_project(self, owner_id, **kwargs):
        """Create a new project.
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :kwargs is Body of
        [https://apidocs.data.world/api/projects/createproject]
        """

    @args(Path, Path, Body)
    @json
    @patch("projects/{owner_id}/{project_id}")
    def patch_project(self, owner_id, project_id, **kwargs):
        """Update an existing project.
        Only elements included in the request will be updated.
        All omitted elements will remain untouched.
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param project_id: Unique identifier of dataset
        :type dataset: str
        :kwargs is Body of
        [https://apidocs.data.world/api/projects/patchproject]
        """

    @args(Path, Path, Body)
    @json
    @put("projects/{owner_id}/{project_id}")
    def replace_project(self, owner_id, project_id, **kwargs):
        """Create or replace a project with a given id.
        If a project exists with the same id, this call will reset
        such project redefining all its attributes.
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param project_id: Unique identifier of dataset
        :type dataset: str
        :kwargs is Body of
        [https://apidocs.data.world/api/projects/replaceproject]
        """

    @args(Path, Path)
    @delete("projects/{owner_id}/{project_id}")
    def delete_project(self, owner_id, project_id):
        """Delete a project and associated data.
        This operation cannot be undone, but you may recreate the project
        using the same id.
        :User must have admin auth token
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param project_id: Unique identifier of dataset
        :type dataset: str
        """

    @args(Path, Path, Path, Path, Body)
    @json
    @put("projects/{owner_id}/{project_id}/linkedDatasets/" +
         "{linked_dataset_owner}/{linked_dataset_id}")
    def add_linked_dataset(self, owner_id, project_id, linked_dataset_owner,
                           linked_dataset_id, **kwargs):
        """
        https://apidocs.data.world/api/projects/addlinkeddataset
        Add Link dataset
        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str owner: User name and unique identifier of the creator.
        :param str id: Project unique identifier.
        :param str linked_dataset_owner: (required)
        :param str linked_dataset_id: (required)
        :return: SuccessMessage
                 If the method is called asynchronously,
                 returns the request thread.
        """

    @args(Path, Path, Path, Path, Body)
    @json
    @delete("projects/{owner_id}/{project_id}/linkedDatasets/" +
            "{linked_dataset_owner}/{linked_dataset_id}")
    def remove_linked_dataset(self, owner_id, project_id,
                              linked_dataset_owner, linked_dataset_id,
                              **kwargs):
        """
        https://apidocs.data.world/api/projects/removelinkeddataset
        Remove Link dataset
        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str owner: User name and unique identifier of the creator.
        :param str id: Project unique identifier.
        :param str linked_dataset_owner: (required)
        :param str linked_dataset_id: (required)
        :return: SuccessMessage
                 If the method is called asynchronously,
                 returns the request thread.
        """

    #
    # def execute_sql(self, owner_id, dataset_id, **kwargs):
    #     preparedRequest = // set request up
    #     return QueryRequest(preparedRequest)
    #
    # class QueryRequest(object):
    #     def to_csv(self):
    #         preparedRequest.headers['Accept'] = 'text/csv'
    #         return preparedRequest.send()
    #
    #     def to_json(self):

from uplink import Consumer, get, post, patch, put, delete, Body,\
    json, args, Path


class InsightsApi(Consumer):
    @args(Path, Path, Path, Body)
    @json
    @get("insights/{owner_id}/{project_id}/{insight_id}")
    def get_insight(self, owner_id, project_id, insight_id, **kwargs):
        """Retrieve a project.
        The definition of the project will be returned,
        not the associated data.
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param project_id: Unique identifier of dataset
        """
        pass

    @args(Path, Path, Body)
    @json
    @get("insights/{owner_id}/{project_id}")
    def get_insights_for_project(self, owner_id, project_id, **kwargs):
        """List insights associated with a project.
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param project_id: Unique identifier of project
        :type dataset_id: str
        :kwargs is Query of
        https://apidocs.data.world/api/insights/getinsightsforproject
        """""
        pass

    @args(Path, Path, Body)
    @json
    @post("insights/{owner_id}/{project_id}")
    def create_insight(self, owner_id, project_id, **kwargs):
        """Create a new insight.
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param project_id: Project unique identifier
        :type project_id: str
        :kwargs is Body of:
        https://apidocs.data.world/api/insights/createinsight
        """
        pass

    @args(Path, Path, Body)
    @json
    @put("insights/{owner_id}/{project_id}")
    def replace_insight(self, owner_id, project_id, **kwargs):
        """Create or replace a project with a given id.
        If a project exists with the same id, this call will reset
        such project redefining all its attributes.
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param dataset_id: Unique identifier of dataset
        :type dataset_id: str
        :kwargs is Body of:
        https://apidocs.data.world/api/projects/replaceproject
        /apidocs.data.world/api/projects/replaceproject]
        """
        pass

    @args(Path, Path, Path, Body)
    @json
    @patch("insights/{owner_id}/{project_id}/{insight_id}")
    def update_insight(self, owner_id, project_id, insight_id, **kwargs):
        """Update an existing insight. Only elements included in the request
        will be updated. All omitted elements will remain untouched.
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param dataset_id: Unique identifier of dataset
        :type dataset_id: str
        :param insight_id: Unique identifier of insight
        :type insight_id: str
        :kwargs is Body of:
        https://apidocs.data.world/api/projects/patchdataset
        """
        pass

    @args(Path, Path, Path)
    @delete("insights/{owner_id}/{dataset_id}/{insight_id}")
    def delete_insight(self, owner_id, dataset_id, insight_id):
        """Delete a insight with the associated insight_id
        This operation cannot be undone, but you may recreate the insight
        using the same id.
        :User must have admin auth token
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param dataset_id: Unique identifier of dataset
        :type dataset_id: str
        :param insight_id: Unique identifier of insight
        :type insight_id: str
        """
        pass

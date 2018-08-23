from uplink import Consumer, get, post, patch, put, delete, Body,\
    json, args, Path


class DatasetsApi(Consumer):
    @get("datasets/{owner_id}/{dataset_id}")
    def get_dataset(self, owner_id, dataset_id):
        """Retrieve a dataset.
        The definition of the project will be returned,
        not the associated data.
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param dataset_id: Unique identifier of dataset
        """
        pass

    @args(Path, Body)
    @json
    @post("datasets/{owner_id}")
    def create_dataset(self, owner_id, **kwargs):
        """Create a new dataset.
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :kwargs is Body of
        [https://apidocs.data.world/api/datasets/createdataset]
        """
        pass

    @args(Path, Path, Body)
    @json
    @patch("datasets/{owner_id}/{dataset_id}")
    def patch_dataset(self, owner_id, dataset_id, **kwargs):
        """Update an existing dataset.
        Only elements included in the request will be updated.
        All omitted elements will remain untouched.
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param dataset_id: Unique identifier of dataset
        :type dataset: str
        :kwargs is Body of
        [https://apidocs.data.world/api/projects/patchdataset]
        """
        pass

    @args(Path, Path, Body)
    @json
    @put("datasets/{owner_id}/{dataset_id}")
    def replace_dataset(self, owner_id, dataset_id, **kwargs):
        """Create or replace a dataset with a given id.
        If a project exists with the same id, this call will reset
        such project redefining all its attributes.
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param dataset_id: Unique identifier of dataset
        :type dataset: str
        :kwargs is Body of
        [https://apidocs.data.world/api/projects/replacedataset]
        """
        pass

    @args(Path, Path)
    @delete("datasets/{owner_id}/{dataset_id}")
    def delete_dataset(self, owner_id, dataset_id):
        """Delete a dataset and associated data.
        This operation cannot be undone, but you may recreate the dataset
        using the same id.
        :User must have admin auth token
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param dataset_id: Unique identifier of dataset
        :type dataset: str
        """
        pass


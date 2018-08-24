from uplink import Consumer, get, post, patch, put, delete, Body,\
    json, args, Path

class StreamsApi(Consumer):
    @args(Path, Path, Body)
    @json
    @get("datasets/{owner_id}/{dataset_id}/queries")
    def append_records(self, owner_id, dataset_id, stream_id):
        """List saved queries associated with a dataset
        The definition of the query will be returned,
        not the query results.
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param dataset_id: Unique identifier of dataset
        :param kwargs: Is Query of:
        https://apidocs.data.world/api/queries/getdatasetqueries
        """
        pass

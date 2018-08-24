from uplink import Consumer, get, post, patch, put, delete, Body,\
    json, args, Path, Header

class QueriesApi(Consumer):
    @args(Path, Path, Body)
    @json
    @get("datasets/{owner_id}/{dataset_id}/queries")
    def get_dataset_queries(self, owner_id, dataset_id, **kwargs):
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

    @args(Path, Path, Body)
    @json
    @get("projects/{owner_id}/{dataset_id}/queries")
    def get_project_queries(self, owner_id, dataset_id, **kwargs):
        """List saved queries associated with a project.
        The definition of the project will be returned,
        not the associated data.
        :param owner_id: User or organization ID of the owner of the dataset
        :type owner_id: str
        :param dataset_id: Unique identifier of dataset
        """
        pass

    @args(Path)
    @get("queries/{query_id}")
    def get_query(self, query_id):
        """Retrieve a saved query.
        :param query_id: Unique identifier for saved queries
        :type str
        """
        pass

    def execute_sql(self, query_id, accept_type, **kwargs):



class QueryResult(object):
    def to_csv(self):
        preparedRequest.headers['Accept'] = 'text/csv'
        return preparedRequest.send()

    def to_json(self):
        preparedRequest.headers['Accept'] = 'application/json'

    def to_jsonl(self):
        preparedRequest.headers['Accept'] = 'application/json-l'

    def to_xndjson(self):
        preparedRequest.headers['Accept'] = 'application/x-ndjson'

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


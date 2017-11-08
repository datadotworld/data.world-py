from ._swagger.api_client import ApiClient


class ContentNegotiatingApiClient(ApiClient):

    def __init__(self, host, header_name, header_value, default_mimetype):
        super(ContentNegotiatingApiClient, self).__init__(host, header_name,
                                                          header_value,
                                                          default_mimetype)
        self.default_mimetype = default_mimetype

    def select_header_accept(self, accepts):
        if not accepts:
            return
        accepts = [x.lower() for x in accepts]

        if self.default_mimetype in accepts:
            return self.default_mimetype
        else:
            return ', '.join(accepts)

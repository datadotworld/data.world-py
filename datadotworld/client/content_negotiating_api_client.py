from ._swagger.api_client import ApiClient


class ContentNegotiatingApiClient(ApiClient):

    def __init__(self, host, header_name, header_value, user_agent,
                 default_mimetype_header_accept='application/json'):
        super(ContentNegotiatingApiClient, self).__init__(host, header_name,
                                                          header_value)
        self.user_agent = user_agent
        self.default_mimetype_header_accept = default_mimetype_header_accept

    def select_header_accept(self,  accepts):
        if not accepts:
            return
        accepts = [x.lower() for x in accepts]

        if self.default_mimetype_header_accept in accepts:
            return self.default_mimetype_header_accept
        else:
            return ', '.join(accepts)

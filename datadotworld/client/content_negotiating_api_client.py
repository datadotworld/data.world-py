from ._swagger.api_client import ApiClient


class ContentNegotiatingApiClient(ApiClient):

    def __init__(self, host, header_name, header_value, user_agent,
                 default_mimetype_header_accept='application/json',
                 default_mimetype_header_content_type='application/json'):
        super(ContentNegotiatingApiClient, self).__init__(host, header_name,
                                                          header_value)
        self.user_agent = user_agent
        self.default_mimetype_header_accept = default_mimetype_header_accept
        self.default_mimetype_header_content_type = \
            default_mimetype_header_content_type

    def select_header_accept(self,  accepts):
        if not accepts:
            return
        accepts = [x.lower() for x in accepts]

        if self.default_mimetype_header_accept in accepts:
            return self.default_mimetype_header_accept
        else:
            return ', '.join(accepts)

    def select_header_content_type(self, content_types):
        if not content_types:
            return 'application/json'
        content_types = [x.lower() for x in content_types]

        if self.default_mimetype_header_content_type in content_types:
            return self.default_mimetype_header_content_type
        else:
            return content_types[0]

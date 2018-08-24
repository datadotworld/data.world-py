from uplink import Consumer, get, post, patch, put, delete, Body,\
    json, args, Path

class UsersApi(Consumer):
    @get("user")
    def get_user_data(self):
        """Retrieve user profile information of the currently
        """
        pass

    @args(Body)
    @json
    @get("user/datasets/contributing")
    def fetch_contributing_datasets(self, **kwargs):
        """
        List datasets that the currently authenticated user has access
        to because he or she is a contributor.
        :param kwargs: Query parameter of:
        https://apidocs.data.world/api/user/fetchcontributingdatasets
        """
        pass

    @args(Body)
    @json
    @get("user/projects/contributing")
    def fetch_contributing_projects(self, **kwargs):
        """
        List projects that the currently authenticated user has access
        to because he or she is a contributor.
        :param kwargs: Query parameter of:
        https://apidocs.data.world/api/user/fetchcontributingprojects
        """
        pass

    @args(Body)
    @json
    @get("user/datasets/own")
    def fetch_datasets(self, **kwargs):
        """
        List datasets that the currently authenticated user has access
        to because he or she is the owner.
        :param kwargs: Query parameter of:
        https://apidocs.data.world/api/user/fetchdatasets
        """
        pass

    @args(Body)
    @json
    @get("user/projects/own")
    def fetch_projects(self, **kwargs):
        """
        List projects that the currently authenticated user has access
        to because he or she is the owner.
        :param kwargs: Query parameter of:
        https://apidocs.data.world/api/user/fetchprojects
        """
        pass

    @args(Body)
    @json
    @get("user/projects/liked")
    def fetch_liked_projects(self, **kwargs):
        """
        List projects that the currently authenticated user liked (bookmarked)
        :param kwargs: Query parameter of:
        https://apidocs.data.world/api/user/fetchlikedprojects
        """
        pass

    @args(Body)
    @json
    @get("user/datasets/liked")
    def fetch_liked_datasets(self, **kwargs):
        """
        List datasets that the currently authenticated user liked (bookmarked)
        :param kwargs: Query parameter of:
        https://apidocs.data.world/api/user/fetchlikeddatasets
        """
        pass
# coding: utf-8

"""
    data.world API

    data.world's mission is to build the most meaningful, collaborative, and abundant data resource in the world, so that people who work with data can solve problems faster.&nbsp;&nbsp; In the context of that mission, this API ensures that our users are able to easily access data and manage their data projects regardless of system or tool preference.

    OpenAPI spec version: 0.4.0
    Contact: help@data.world
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from ..configuration import Configuration
from ..api_client import ApiClient


class SqlApi(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def sql_get(self, owner, id, **kwargs):
        """
        SQL query (via GET)
        This endpoint executes SQL queries against a dataset. New to SQL? Check out data.world's [SQL manual](https://docs.data.world/tutorials/dwsql/) .
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.sql_get(owner, id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str owner: User name and unique identifier of the creator of the dataset. For example, in the URL: [https://data.world/jonloyens/an-intro-to-dataworld-dataset](https://data.world/jonloyens/an-intro-to-dataworld-dataset), jonloyens is the unique identifier of the dataset. (required)
        :param str id: Dataset unique identifier.   For example, in the URL: [https://data.world/jonloyens/an-intro-to-dataworld-dataset](https://data.world/jonloyens/an-intro-to-dataworld-dataset), an-intro-to-dataworld-dataset is the unique identifier of the dataset. (required)
        :param str query:
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.sql_get_with_http_info(owner, id, **kwargs)
        else:
            (data) = self.sql_get_with_http_info(owner, id, **kwargs)
            return data

    def sql_get_with_http_info(self, owner, id, **kwargs):
        """
        SQL query (via GET)
        This endpoint executes SQL queries against a dataset. New to SQL? Check out data.world's [SQL manual](https://docs.data.world/tutorials/dwsql/) .
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.sql_get_with_http_info(owner, id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str owner: User name and unique identifier of the creator of the dataset. For example, in the URL: [https://data.world/jonloyens/an-intro-to-dataworld-dataset](https://data.world/jonloyens/an-intro-to-dataworld-dataset), jonloyens is the unique identifier of the dataset. (required)
        :param str id: Dataset unique identifier.   For example, in the URL: [https://data.world/jonloyens/an-intro-to-dataworld-dataset](https://data.world/jonloyens/an-intro-to-dataworld-dataset), an-intro-to-dataworld-dataset is the unique identifier of the dataset. (required)
        :param str query:
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['owner', 'id', 'query']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sql_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'owner' is set
        if ('owner' not in params) or (params['owner'] is None):
            raise ValueError("Missing the required parameter `owner` when calling `sql_get`")
        # verify the required parameter 'id' is set
        if ('id' not in params) or (params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `sql_get`")


        collection_formats = {}

        resource_path = '/sql/{owner}/{id}'.replace('{format}', 'json')
        path_params = {}
        if 'owner' in params:
            path_params['owner'] = params['owner']
        if 'id' in params:
            path_params['id'] = params['id']

        query_params = {}
        if 'query' in params:
            query_params['query'] = params['query']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['text/csv'])

        # Authentication setting
        auth_settings = ['token']

        return self.api_client.call_api(resource_path, 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type=None,
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def sql_post(self, owner, id, **kwargs):
        """
        SQL query
        This endpoint executes SQL queries against a dataset. New to SQL? Check out data.world's [SQL manual](https://docs.data.world/tutorials/dwsql/) .
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.sql_post(owner, id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str owner: User name and unique identifier of the creator of the dataset. For example, in the URL: [https://data.world/jonloyens/an-intro-to-dataworld-dataset](https://data.world/jonloyens/an-intro-to-dataworld-dataset), jonloyens is the unique identifier of the dataset. (required)
        :param str id: Dataset unique identifier.   For example, in the URL: [https://data.world/jonloyens/an-intro-to-dataworld-dataset](https://data.world/jonloyens/an-intro-to-dataworld-dataset), an-intro-to-dataworld-dataset is the unique identifier of the dataset. (required)
        :param str query:
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.sql_post_with_http_info(owner, id, **kwargs)
        else:
            (data) = self.sql_post_with_http_info(owner, id, **kwargs)
            return data

    def sql_post_with_http_info(self, owner, id, **kwargs):
        """
        SQL query
        This endpoint executes SQL queries against a dataset. New to SQL? Check out data.world's [SQL manual](https://docs.data.world/tutorials/dwsql/) .
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.sql_post_with_http_info(owner, id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str owner: User name and unique identifier of the creator of the dataset. For example, in the URL: [https://data.world/jonloyens/an-intro-to-dataworld-dataset](https://data.world/jonloyens/an-intro-to-dataworld-dataset), jonloyens is the unique identifier of the dataset. (required)
        :param str id: Dataset unique identifier.   For example, in the URL: [https://data.world/jonloyens/an-intro-to-dataworld-dataset](https://data.world/jonloyens/an-intro-to-dataworld-dataset), an-intro-to-dataworld-dataset is the unique identifier of the dataset. (required)
        :param str query:
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['owner', 'id', 'query']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sql_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'owner' is set
        if ('owner' not in params) or (params['owner'] is None):
            raise ValueError("Missing the required parameter `owner` when calling `sql_post`")
        # verify the required parameter 'id' is set
        if ('id' not in params) or (params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `sql_post`")


        collection_formats = {}

        resource_path = '/sql/{owner}/{id}'.replace('{format}', 'json')
        path_params = {}
        if 'owner' in params:
            path_params['owner'] = params['owner']
        if 'id' in params:
            path_params['id'] = params['id']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'query' in params:
            form_params.append(('query', params['query']))

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['text/csv'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/x-www-form-urlencoded'])

        # Authentication setting
        auth_settings = ['token']

        return self.api_client.call_api(resource_path, 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type=None,
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

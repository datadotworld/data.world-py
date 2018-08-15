from __future__ import absolute_import

import copy
from os import path

import pytest
import pytest
import responses
import unittest

from datadotworld.client import modules

# class TestProjects(unittest.TestCase):

# 	@pytest.fixture()
# 	def client(self):
# 		return ApiClient(api_token='just_a_test_token')

# 	@responses.activate
# 	def test_create_project(self, client):
# 		expected_resp = {'message': 'Success'}
# 		responses.add('PUT', '{}/datasets/owner/project'.format(client._api_url),
# 			json=expected_resp, status=200)
# 		resp = client.create_project('owner', 'dataset', title='Dataset', visibility='OPEN')
# 		print('RESPPPPP', resp)
# 		assert_that(resp, equal_to(expected_resp))

# data.world-py
# Copyright 2017 data.world, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the
# License.
#
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
#
# This product includes software developed at
# data.world, Inc.(http://data.world/).
import csv
import json
import responses
import pytest
from datadotworld.config import DefaultConfig
from datadotworld.filewriter import DataDotWorldFileWriter, DataDotWorldFileWriterException

class TestDataDotWorldFileWriter:

    def test_basic(self):
        with responses.RequestsMock() as resp:
            def upload_endpoint(request):
                assert "test" == ''.join(request.body)
                return 200, {}, json.dumps({})
            resp.add_callback(resp.PUT,
                              '{}/uploads/{}/{}/files/{}'.format('https://api.data.world/v0',
                                                                 'user', 'dataset', 'file.txt'),
                              callback=upload_endpoint)
            with DataDotWorldFileWriter(DefaultConfig(), "user/dataset", "file.txt") as writer:
                writer.write("test")

    def test_csv(self):
        with responses.RequestsMock() as resp:
            def upload_endpoint(request):
                assert "a,b\r\n42,17\r\n420,178\r\n" == ''.join(request.body)
                return 200, {}, json.dumps({})
            resp.add_callback(resp.PUT,
                              '{}/uploads/{}/{}/files/{}'.format('https://api.data.world/v0',
                                                                 'user', 'dataset', 'file.csv'),
                              callback=upload_endpoint)
            with DataDotWorldFileWriter(DefaultConfig(), "user/dataset", "file.csv") as writer:
                csvw = csv.DictWriter(writer, fieldnames=['a', 'b'])
                csvw.writeheader()
                csvw.writerow({'a': 42, 'b':17})
                csvw.writerow({'a': 420, 'b':178})


    def test_error(self):
        with pytest.raises(DataDotWorldFileWriterException) as e:
            with responses.RequestsMock() as resp:
                def upload_endpoint(request):
                    return 400, {}, json.dumps({})

                resp.add_callback(resp.PUT,
                                  '{}/uploads/{}/{}/files/{}'.format('https://api.data.world/v0',
                                                                     'user', 'dataset', 'file.txt'),
                                  callback=upload_endpoint)
                with DataDotWorldFileWriter(DefaultConfig(), "user/dataset", "file.txt") as writer:
                    writer.write("test")


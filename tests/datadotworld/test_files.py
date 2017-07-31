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
import struct
from datadotworld.config import DefaultConfig
from datadotworld.files import RemoteFile, RemoteFileException
from datadotworld.client.api import RestApiError


class TestDataDotWorldFileWriter:
    def test_write_basic(self):
        with responses.RequestsMock() as resp:
            def upload_endpoint(request):
                assert "test" == ''.join([chunk.decode('utf-8') for chunk in request.body])
                return 200, {}, json.dumps({})

            resp.add_callback(resp.PUT,
                              '{}/uploads/{}/{}/files/{}'.format('https://api.data.world/v0',
                                                                 'user', 'dataset', 'file.txt'),
                              callback=upload_endpoint)
            with RemoteFile(DefaultConfig(), "user/dataset", "file.txt") as writer:
                writer.write("test")

    def test_write_csv(self):
        with responses.RequestsMock() as resp:
            def upload_endpoint(request):
                assert "a,b\r\n42,17\r\n420,178\r\n" == \
                       ''.join([chunk.decode('utf-8') for chunk in request.body])
                return 200, {}, json.dumps({})

            resp.add_callback(resp.PUT,
                              '{}/uploads/{}/{}/files/{}'.format('https://api.data.world/v0',
                                                                 'user', 'dataset', 'file.csv'),
                              callback=upload_endpoint)
            with RemoteFile(DefaultConfig(), "user/dataset", "file.csv") as writer:
                csvw = csv.DictWriter(writer, fieldnames=['a', 'b'])
                csvw.writeheader()
                csvw.writerow({'a': 42, 'b': 17})
                csvw.writerow({'a': 420, 'b': 178})

    def test_write_error(self):
        with pytest.raises(RestApiError):
            with responses.RequestsMock() as resp:
                def upload_endpoint(request):
                    return 400, {}, json.dumps({})

                resp.add_callback(resp.PUT,
                                  '{}/uploads/{}/{}/files/{}'.format('https://api.data.world/v0',
                                                                     'user', 'dataset', 'file.txt'),
                                  callback=upload_endpoint)
                with RemoteFile(DefaultConfig(), "user/dataset", "file.txt") as writer:
                    writer.write("test")

    def test_write_timeout_error(self):
        with pytest.raises(RemoteFileException):
            with RemoteFile(DefaultConfig(), "user/dataset", "file.txt", timeout=0.0) as writer:
                writer.write("test")

    def test_read_basic(self):
        with responses.RequestsMock() as resp:
            def download_endpoint(request):
                return 200, {}, "this is the test."

            resp.add_callback(resp.GET,
                              '{}/file_download/{}/{}/{}'.format('https://query.data.world',
                                                                 'user', 'dataset', 'file.txt'),
                              callback=download_endpoint)
            with RemoteFile(DefaultConfig(), "user/dataset", "file.txt", mode="r") as reader:
                contents = reader.read()
                assert "this is the test." == contents

    def test_read_non_utf_8(self):
        with responses.RequestsMock() as resp:
            def download_endpoint(request):
                return 200, {}, "this is the test.".encode('utf-16')

            resp.add_callback(resp.GET,
                              '{}/file_download/{}/{}/{}'.format('https://query.data.world',
                                                                 'user', 'dataset', 'file.txt'),
                              callback=download_endpoint)
            with RemoteFile(DefaultConfig(), "user/dataset", "file.txt", mode="rb") as reader:
                contents = reader.read()
                assert "this is the test." == contents.decode('utf-16')

    def test_read_binary_basic(self):
        with responses.RequestsMock() as resp:
            def download_endpoint(request):
                return 200, {}, "this is the test."

            resp.add_callback(resp.GET,
                              '{}/file_download/{}/{}/{}'.format('https://query.data.world',
                                                                 'user', 'dataset', 'file.txt'),
                              callback=download_endpoint)
            with RemoteFile(DefaultConfig(), "user/dataset", "file.txt", mode="rb") as reader:
                contents = reader.read()
                assert b"this is the test." == contents

    def test_read_binary_bytes(self):
        with responses.RequestsMock() as resp:
            def download_endpoint(request):
                return 200, {}, struct.pack('BBBB', 0, 1, 254, 255)

            resp.add_callback(resp.GET,
                              '{}/file_download/{}/{}/{}'.format('https://query.data.world',
                                                                 'user', 'dataset', 'file.txt'),
                              callback=download_endpoint)
            with RemoteFile(DefaultConfig(), "user/dataset", "file.txt", mode="rb") as reader:
                contents = reader.read()
                assert b"\x00\x01\xfe\xff" == contents

    def test_read_binary_iter(self):
        with responses.RequestsMock() as resp:
            def download_endpoint(request):
                return 200, {}, "abcdef"

            resp.add_callback(resp.GET,
                              '{}/file_download/{}/{}/{}'.format('https://query.data.world',
                                                                 'user', 'dataset', 'file.txt'),
                              callback=download_endpoint)
            with RemoteFile(DefaultConfig(), "user/dataset", "file.txt", mode="rb") as reader:
                contents = list(reader)
                assert [b'a', b'b', b'c', b'd', b'e', b'f'] == contents

    def test_read_binary_iter_chunks(self):
        with responses.RequestsMock() as resp:
            def download_endpoint(request):
                return 200, {}, "abcdef"

            resp.add_callback(resp.GET,
                              '{}/file_download/{}/{}/{}'.format('https://query.data.world',
                                                                 'user', 'dataset', 'file.txt'),
                              callback=download_endpoint)
            with RemoteFile(DefaultConfig(), "user/dataset", "file.txt",
                            mode="rb", chunk_size=4) as reader:
                contents = list(reader)
                assert [b'abcd', b'ef'] == contents

    def test_read_binary_bytes_iter(self):
        with responses.RequestsMock() as resp:
            def download_endpoint(request):
                return 200, {}, struct.pack('BBBB', 0, 1, 254, 255)

            resp.add_callback(resp.GET,
                              '{}/file_download/{}/{}/{}'.format('https://query.data.world',
                                                                 'user', 'dataset', 'file.txt'),
                              callback=download_endpoint)
            with RemoteFile(DefaultConfig(), "user/dataset", "file.txt", mode="rb") as reader:
                contents = list(reader)
                assert [b"\x00", b"\x01", b"\xfe", b"\xff"] == contents

    def test_read_error(self):
        with pytest.raises(RestApiError):
            with responses.RequestsMock() as resp:
                def download_endpoint(request):
                    return 400, {}, json.dumps({'message': 'bad request'})

                resp.add_callback(resp.GET,
                                  '{}/file_download/{}/{}/{}'.format('https://query.data.world',
                                                                     'user', 'dataset', 'file.txt'),
                                  callback=download_endpoint)
                with RemoteFile(DefaultConfig(), "user/dataset", "file.txt", mode="r") as reader:
                    contents = reader.read()
                    assert "this is the test." == contents

    def test_read_csv(self):
        with responses.RequestsMock() as resp:
            def download_endpoint(request):
                return 200, {}, "A,B,C\n1,2,3\n4,5,6"

            resp.add_callback(resp.GET,
                              '{}/file_download/{}/{}/{}'.format('https://query.data.world',
                                                                 'user', 'dataset', 'file.csv'),
                              callback=download_endpoint)
            with RemoteFile(DefaultConfig(), "user/dataset", "file.csv", mode="r") as reader:
                csvr = csv.DictReader(reader)
                rows = list(csvr)
                assert rows[0] == {'A': '1', 'B': '2', 'C': '3'}
                assert rows[1] == {'A': '4', 'B': '5', 'C': '6'}

    def test_read_jsonl(self):
        with responses.RequestsMock() as resp:
            def download_endpoint(request):
                return 200, {}, '{"A":"1", "B":"2", "C":"3"}\n' \
                                '{"A":"4", "B":"5", "C":"6"}\n'

            resp.add_callback(resp.GET,
                              '{}/file_download/{}/{}/{}'.format('https://query.data.world',
                                                                 'user', 'dataset', 'file.csv'),
                              callback=download_endpoint)
            with RemoteFile(DefaultConfig(), "user/dataset", "file.csv", mode="r") as reader:
                rows = [json.loads(line) for line in reader if line.strip()]
                assert rows[0] == {'A': '1', 'B': '2', 'C': '3'}
                assert rows[1] == {'A': '4', 'B': '5', 'C': '6'}

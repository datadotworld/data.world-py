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
from __future__ import absolute_import

try:
    from queue import Queue
except ImportError:
    from Queue import Queue
from threading import Thread
import json
import requests
from datadotworld.util import parse_dataset_key


class DataDotWorldFileWriter:
    def __init__(self, config, dataset_key, file_name,
                 host="https://api.data.world/v0",
                 timeout=None):
        """
        Construct a new data.world file writer - values written to the
        `write()` method are streamed to the data.world api and written into
        the specified file. The proper way to use this class is in a `with`
        block:
        >>> with DataDotWorldFileWriter(config, "user/dataset", "file") as w
        >>>   w.write("")
        which will ensure that at the end of the `with` block the file is
        closed and the HTTP request completes
        :param config: the data.world configuration object
        :param dataset_key: key for the target dataset
        :param file_name: name of file to write
        :param host: hostname for the API - defaults to the standard
        production API
        :param timeout: how long to wait for a response when `close()` is
        called before timing out (defaults to no timeout - the close() call
        by default will wait indefinitely for a response)
        """
        self._queue = Queue(10)
        self._sentinel = None
        self._timeout = timeout
        self._response_queue = Queue(1)

        def put_request(body, response_queue):
            ownerid, datasetid = parse_dataset_key(dataset_key)
            response = requests.put(
                "{}/uploads/{}/{}/files/{}".format(
                    host, ownerid, datasetid, file_name),
                data=body,
                headers={
                    'Authorization': 'Bearer {}'.format(config.auth_token)
                })
            response_queue.put(response)

        body = iter(self._queue.get, self._sentinel)
        self._thread = Thread(target=put_request,
                              args=(body, self._response_queue))

    def write(self, value):
        """
        write the given value to the stream - if the object is a bytearray,
        write it as-is - otherwise, convert the object to a string with
        `str()` and write the UTF-8 bytes
        :param value: the value to write
        """
        if isinstance(value, bytearray):
            self._queue.put(value)
        elif isinstance(value, dict) or isinstance(value, list):
            self._queue.put(json.dumps(value).encode('utf-8'))
        else:
            self._queue.put(str(value).encode('utf-8'))

    def open(self):
        """
        start the thread executing the HTTP request
        """
        self._thread.start()

    def close(self):
        """
        closing the writer adds the sentinel value into the queue and joins
        the thread executing the HTTP request
        """
        self._queue.put(self._sentinel)
        self._thread.join(timeout=self._timeout)
        if self._thread.is_alive():
            raise DataDotWorldFileWriterException("Closing file timed out.")
        response = self._response_queue.get_nowait()
        try:
            response.raise_for_status()
        except Exception as e:
            raise DataDotWorldFileWriterException(cause=e)

    def __enter__(self):
        """
        Implement the context manager protocol
        """
        self.open()
        return self

    def __exit__(self, e_type, e_value, traceback):
        """
        Implement the context manager protocol
        """
        self.close()


class DataDotWorldFileWriterException(Exception):
    """
    Exception wrapper for exceptions arising from the DataDotWorldFileWriter
    """

    def __init__(self, *args, **kwargs):
        self.cause = kwargs.pop('cause', None)
        super(DataDotWorldFileWriterException, self).__init__(*args, **kwargs)

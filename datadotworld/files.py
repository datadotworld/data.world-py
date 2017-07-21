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
import requests
from datadotworld.util import parse_dataset_key
from datadotworld.client.api import RestApiError


class RemoteFile:
    def __init__(self, config, dataset_key, file_name,
                 mode='w',
                 timeout=None):
        """
        Construct a new data.world file object - values written to the
        `write()` method are streamed to the data.world api and written into
        the specified file. The proper way to use this class is in a `with`
        block:
        >>> with RemoteFile(config, "user/dataset", "file") as w
        >>>   w.write("")
        which will ensure that at the end of the `with` block the file is
        closed and the HTTP request completes

        Parameters
        ----------
        config: DefaultConfig
            the data.world configuration object
        dataset_key: str
            key for the target dataset
        file_name: str
            name of file to write
        mode: str, optional
            the mode for the file - currently only 'w' (write string) or
            'wb' (write binary) are supported, any other value will throw
            an exception
        timeout: float, optional
            how long to wait for a response when `close()` is
            called before timing out (defaults to no timeout - the close()
            call by default will wait indefinitely for a response)
        """
        self._api_host = "https://api.data.world/v0"
        self._queue = Queue(10)
        self._response_queue = Queue(1)
        self._sentinel = None
        self._timeout = timeout
        self._config = config
        self._dataset_key = dataset_key
        self._file_name = file_name
        if not(mode == 'w' or mode == 'wb'):
            raise NotImplementedError(
                "modes other than 'w' and 'wb' not supported")
        self._mode = mode


    def write(self, value):
        """
        write the given value to the stream - if the object is a bytearray,
        write it as-is - otherwise, convert the object to a string with
        `str()` and write the UTF-8 bytes

        Parameters
        ----------
        value: str or bytearray
            the value to write

        Raises
        ------
        TypeError
            if the type of the value provided does not match the mode in
            which the file was opened
        NotImplementedError
            if the mode of the file is not one of the supported values
            (currently only "writing" modes for files are supported - leaving
            the option to implement "read" modes open for future work)
        """
        if 'w' == self._mode:
            if isinstance(value, str):
                self._queue.put(value.encode('utf-8'))
            else:
                raise TypeError(
                    "write() argument must be str, not {}"
                        .format(type(value)))
        elif 'wb' == self._mode:
            if (isinstance(value, (bytes, bytearray))):
                self._queue.put(value)
            else:
                raise TypeError(
                    "a bytes-like object is required, not {}"
                        .format(type(value)))
        else:
            raise NotImplementedError(
                "modes other than 'w' and 'wb' not supported")

    def open(self):
        """
        start the thread executing the HTTP request
        """
        def put_request(body, response_queue, host,
                        config, dataset_key, file_name):
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
                              args=(body,
                                    self._response_queue,
                                    self._api_host,
                                    self._config,
                                    self._dataset_key,
                                    self._file_name))
        self._thread.start()

    def close(self):
        """
        closing the writer adds the sentinel value into the queue and joins
        the thread executing the HTTP request
        """
        self._queue.put(self._sentinel)
        self._thread.join(timeout=self._timeout)
        if self._thread.is_alive():
            raise RemoteFileException("Closing file timed out.")
        response = self._response_queue.get_nowait()
        try:
            response.raise_for_status()
        except Exception as e:
            raise RestApiError(cause=e)

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


class RemoteFileException(Exception):
    """
    Exception wrapper for exceptions arising from the RemoteFile
    """

    def __init__(self, *args, **kwargs):
        self.cause = kwargs.pop('cause', None)
        super(RemoteFileException, self).__init__(*args, **kwargs)

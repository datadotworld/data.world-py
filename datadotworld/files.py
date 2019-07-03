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
from datadotworld.util import parse_dataset_key, _user_agent
from datadotworld.client.api import RestApiError
from datadotworld.hosts import API_HOST, QUERY_HOST


class RemoteFile:
    """ """

    def __init__(self, config, dataset_key, file_name,
                 mode='w', **kwargs):
        """
        Construct a new data.world file object - values written to the
        `write()` method are streamed to the data.world api and written into
        the specified file. The proper way to use this class is in a `with`
        block:
        >>> with RemoteFile(config, "user/dataset", "file") as w
        >>>   w.write("")
        or
        >>> with RemoteFile(config, "user/dataset", "file", mode='r') as r
        >>>   contents = r.read()
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
        chunk_size: int, optional
            size of chunked bytes to return when reading streamed bytes
            in 'rb' mode
        decode_unicode: bool, optional
            whether to decode textual responses as unicode when returning
            streamed lines in 'r' mode
        """
        self._api_host = "{}/v0".format(API_HOST)
        self._query_host = QUERY_HOST
        self._config = config
        self._dataset_key = dataset_key
        self._file_name = file_name
        self._mode = mode
        self._user_agent = kwargs.get('user_agent', _user_agent())
        if mode in {'w', 'wb'}:
            self._queue = Queue(10)
            self._response_queue = Queue(1)
            self._sentinel = None
            self._thread = None
            self._timeout = kwargs.get('timeout')
        elif mode in {'r', 'rb'}:
            self._read_response = None
            self._chunk_size = kwargs.get('chunk_size', 1)
            self._decode_unicode = kwargs.get('decode_unicode', True)
        else:
            raise NotImplementedError(
                "modes other than 'w', 'wb', 'r', and 'rb' not supported")

    def write(self, value):
        """write the given value to the stream - if the object is a bytearray,
        write it as-is - otherwise, convert the object to a string with
        `str()` and write the UTF-8 bytes

        :param value: the value to write
        :type value: str or bytearray
        :raises TypeError: if the type of the value provided does not match
            the mode in which the file was opened.
        :raises NotImplementedError: if the mode of the file is not one of the
        supported values (currently only "writing" modes for files are
        supported - leaving the option to implement "read" modes open for
        future work)
        """
        if 'w' == self._mode and isinstance(value, str):
            self._queue.put(value.encode('utf-8'))
        elif self._mode in {'w', 'wb'}:
            if isinstance(value, (bytes, bytearray)):
                self._queue.put(value)
            else:
                raise TypeError(
                    "a string or bytes object is required, not {}".format(
                        type(value)))
        else:
            raise IOError("File not opened in write mode.")

    def read(self):
        """read the contents of the file that's been opened in read mode"""
        if 'r' == self._mode:
            return self._read_response.text
        elif 'rb' == self._mode:
            return self._read_response.content
        else:
            raise IOError("File not opened in read mode.")

    def __iter__(self):
        """
        in 'r' mode, iterates the lines of the response text in unicode -
        in 'rb' mode, iterates the bytes of the binary response.
        """
        if 'r' == self._mode:
            return self._read_response.iter_lines(
                decode_unicode=self._decode_unicode)
        elif 'rb' == self._mode:
            return self._read_response.iter_content(
                chunk_size=self._chunk_size)
        else:
            raise IOError("File not opened in read mode.")

    def open(self):
        """in write mode, start the thread executing the HTTP request.  in read
        mode, execute the GET request and hold on to the response.


        """
        if self._mode.find('w') >= 0:
            self._open_for_write()
        else:
            self._open_for_read()

    def _open_for_read(self):
        """open the file in read mode"""
        ownerid, datasetid = parse_dataset_key(self._dataset_key)
        response = requests.get(
            '{}/file_download/{}/{}/{}'.format(
                self._query_host, ownerid, datasetid, self._file_name),
            headers={
                'User-Agent': self._user_agent,
                'Authorization': 'Bearer {}'.format(
                    self._config.auth_token)
            }, stream=True)
        try:
            response.raise_for_status()
        except Exception as e:
            raise RestApiError(cause=e)
        self._read_response = response

    def _open_for_write(self):
        """open the file in write mode"""
        def put_request(body):
            """

            :param body:
            """
            ownerid, datasetid = parse_dataset_key(self._dataset_key)
            response = requests.put(
                "{}/uploads/{}/{}/files/{}".format(
                    self._api_host, ownerid, datasetid, self._file_name),
                data=body,
                headers={
                    'User-Agent': self._user_agent,
                    'Authorization': 'Bearer {}'.format(
                        self._config.auth_token)
                })
            self._response_queue.put(response)

        body = iter(self._queue.get, self._sentinel)
        self._thread = Thread(target=put_request, args=(body,))
        self._thread.start()

    def close(self):
        """in write mode, closing the handle adds the sentinel value into the
        queue and joins the thread executing the HTTP request.  in read mode,
        this clears out the read response object so there are no references
        to it, and the resources can be reclaimed.


        """
        if self._mode.find('w') >= 0:
            self._queue.put(self._sentinel)
            self._thread.join(timeout=self._timeout)
            if self._thread.is_alive():
                raise RemoteFileException("Closing file timed out.")
            response = self._response_queue.get_nowait()
            try:
                response.raise_for_status()
            except Exception as e:
                raise RestApiError(cause=e)
        else:
            self._read_response = None

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
    """ """

    def __init__(self, *args, **kwargs):
        self.cause = kwargs.pop('cause', None)
        super(RemoteFileException, self).__init__(*args, **kwargs)

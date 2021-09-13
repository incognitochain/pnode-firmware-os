from abc import abstractmethod

import zmq
import os
import sys
import hashlib
import thread


class AutonomousService(object):
    _SERVICE = None
    __callback = None

    @staticmethod
    def instance():
        if AutonomousService._SERVICE is None:
            AutonomousService._SERVICE = AutonomousService()
        return AutonomousService._SERVICE

    def __init__(self):
        pass

    def __get_absolute_path(self):
        return os.path.abspath(os.path.realpath(sys.argv[0]))

    @staticmethod
    def get_zmq_channel(file_path):
        md5 = hashlib.md5()
        md5.update(file_path)
        return "ipc:///tmp/" + md5.hexdigest()

    def my_zmq_channel(self):
        return AutonomousService.get_zmq_channel(self.__get_absolute_path())

    @abstractmethod
    def process(self, data, source, protocol, error):
        pass

    def run(self, callback=None):
        if callback is None:
            callback = self.process

        self.__callback = callback

        c = zmq.Context()
        s = c.socket(zmq.PULL)
        try:
            s.bind(AutonomousService.get_zmq_channel(self.__get_absolute_path()))
            while True:
                d = s.recv_json()
                if d:
                    if "data" not in d:
                        raise Exception("Invalid received data: Missing ""data"" key")
                    if "source" not in d:
                        raise Exception("Invalid received data: Missing ""source"" key")
                    if "protocol" not in d:
                        raise Exception("Invalid received data: Missing ""protocol"" key")

                    data = d["data"]
                    source = d["source"]
                    protocol = d["protocol"]
                    type = d["type"]

                    json_data = {"data": data, "source": source, "protocol": protocol, "type": type}

                    thread.start_new_thread(self.__callback, (json_data, None, ))

        except Exception as e:
            self.__callback(None, e)
        finally:
            s.close()
            c.term()

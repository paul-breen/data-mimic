###############################################################################
# Project: Data Mimic
# Purpose: Base class to encapsulate default PDS mimic behaviour
# Author:  Paul M. Breen
# Date:    2018-06-24
###############################################################################

from datamimic.BaseMimic import BaseMimic
import pds.pds as pds

class PdsBaseMimic(BaseMimic):
    def __init__(self, id):
        super().__init__(id)
        self.conn = None

    def __del__(self):
        self.disconnect()

    def init(self, ipckey=pds.PDS_IPCKEY, **kwargs):
        self.connect(ipckey=ipckey)
        super().init(**kwargs)

    def connect(self, ipckey=pds.PDS_IPCKEY):
        self.conn = pds.PDSconnect(ipckey)

        if self.conn.conn_status != pds.PDS_CONN_OK:
            raise ValueError("Error connecting to the PDS: {}".format(self.conn.status))

    def disconnect(self):
        pds.PDSdisconnect(self.conn)
        self.conn = None

    def get_variable(self, name):
        retval, value = pds.PDSget_tag(self.conn, name)

        if retval == -1:
            raise ValueError("Failed to get PDS tag {} value".format(name))
        else:
            value = int(value)

        return value


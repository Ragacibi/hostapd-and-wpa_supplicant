#! /usr/bin/env python
"""XMLRPC Server program to deal
with hostapd service
- Use function remote() to communicate
"""
from subprocess import Popen
from subprocess import check_output
from SimpleXMLRPCServer import SimpleXMLRPCServer


def singleton(cls):
    """function used to make a
    class to have only one object
    """
    instances = {}
    def getinstance():
        """Get the instance of class
        """
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class HandleServiceAP(object):
    """Used to deal with
    the hostapd service
    """
    def __init__(self):
        """Initialize service state
        """
        self.service = None

    def start(self, filename):
        """Used to start the service
        """
        self.service = Popen(["hostapd", filename])

    def stop(self):
        """Used to stop a service
        """
        if not self.service:
            print "Already running..."
        else:
            self.service.terminate()
            self.service = None

@singleton
class HandleServiceSTA(object):
    """Used to deal with
    the hostapd service
    """
    def __init__(self):
        """Initialize service state
        """
        self.service = None

    def start(self, filename, iface):
        """Used to start the service
        """
        self.service = Popen(["wpa_supplicant", "-Dnl80211", "-i" + iface, "-c", filename])

    def stop(self):
        """Used to stop a service
        """
        if not self.service:
            print "Already running OR Service is not started yet"
        else:
            self.service.terminate()
            self.service = None

def remote(status, data, hotspot, iface):
    """function used to communicate
    between the server and client
    """
    if hotspot == 'True':
        ap_obj = HandleServiceAP()
        filename = 'access_point.conf'
        with open(filename, 'w') as t_file:
            t_file.writelines(data)

        if status == 'start':
            ap_obj.start(filename)
        if status == 'stop':
            ap_obj.stop()
    if hotspot == 'False':
        sta_obj = HandleServiceSTA()
        filename = 'station.conf'
        with open(filename, 'w') as t_file:
            t_file.writelines(data)

        if status == 'start':
            sta_obj.start(filename, iface)
        if status == 'stop':
            sta_obj.stop()        

    return True

def verify_connection():
    interface = check_output('cat access_point.conf | grep interface | cut -d= -f2', shell=True)
    interface = interface.strip()
    res = check_output('iw dev '+ interface + ' station dump | grep Station | cut -f2 -d" "', shell=True)
    return res.split()

SERVER = SimpleXMLRPCServer(('0.0.0.0', 80))
print "Listening on port 80..."
SERVER.register_function(remote, "board")
SERVER.register_function(verify_connection, "verify_connection")
SERVER.serve_forever()

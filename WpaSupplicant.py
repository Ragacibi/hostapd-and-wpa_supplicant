"""This module is used to configure the wpa supplicant """
from os import path
from xmlrpclib import ServerProxy
from ConfFile import ConfFile

class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls._instance = None

def __call__(cls, *args, **kw):
    if cls._instance is None:
        cls._instance = super(Singleton, cls).__call__(*args, **kw)
    return cls._instance


class WpaSupplicant(ConfFile):
    """Class WpaSupplicant
    """
    # Attributes:

    __metaclass__ = Singleton

    _peripheral = 'wlan0'

    __options = {'p':'psk=',
                 's':'ssid=',
                 'algs':'auth_alg=SHARED',
                 'key':'key_mgmt=',
                 'wep':'wep_key',
                 'wep_txid':'wep_tx_keyidx=',
                 'eap':'eap=',
                 'phase2':'phase2="auth=MSCHAPV2"',
                 'user':'identity=',
                 'pass_key':'password=',
                 'pair':'pairwise=',
                 'g':'group=',
                 'ctrl_iface':'ctrl_interface=',
                 'ctrl_iface_grp':'ctrl_interface_group=',
                }
    # Operations
    def __init__(self, name, server_ip, server_port=80):
        """Generates a configuration file. `name` specifies the name of the configuration file.
        """
        ConfFile.__init__(self, name)
        self.proxy = ServerProxy("http://" + str(server_ip) + ":" + str(server_port),
                                 allow_none=False)
        self.__network_block()

    def ssid(self, nw_name):
        """Used to connect the station to the ssid given.
        """
        self.delete('^}.*')
        self.stream_edit(self.__options['s'] + '.*', self.__options['s'] + '"' + nw_name + '"')
        self.stream_edit('^}.*', '}\n')

    def ctrl_interface(self, ctrl_iface_sta):
        """Used to set the control interface of STA
        """
        self.stream_edit(self.__options['ctrl_iface'] + '.*',
                         self.__options['ctrl_iface'] + ctrl_iface_sta, prepend=True)

    def ctrl_interface_group(self, ctrl_iface_grp_sta):
        """Used to set the control interface of STA
        """
        self.stream_edit(self.__options['ctrl_iface_grp'] + '.*',
                         self.__options['ctrl_iface_grp'] + ctrl_iface_grp_sta, prepend=True)

    def key_mgt(self, key='WPA-PSK'):
        """Used to select the WPA security. By default, the security will be WPA-PSK
        """
        self.delete('^}.*')
        if key == "NONE":
            self.stream_edit(self.__options['key'] + '.*', self.__options['key'] + key)
            self.delete(self.__options['p'] + '.*')
            self.delete(self.__options['algs'] + '.*')
            self.delete(self.__options['wep'] + '.*')
            self.delete(self.__options['wep_txid'] + '.*')
            self.delete(self.__options['eap'] + '.*')
            self.delete(self.__options['phase2'] + '.*')
            self.delete(self.__options['user'] + '.*')
            self.delete(self.__options['pass_key'] + '.*')
            self.delete(self.__options['pair'] + '.*')
            self.delete(self.__options['g'] + '.*')
        elif key == "WEP":
            self.stream_edit(self.__options['key'] + '.*', self.__options['key'] + "NONE")
            self.delete(self.__options['p'] + '.*')
            self.delete(self.__options['eap'] + '.*')
            self.delete(self.__options['phase2'] + '.*')
            self.delete(self.__options['user'] + '.*')
            self.delete(self.__options['pass_key'] + '.*')
            self.delete(self.__options['pair'] + '.*')
            self.delete(self.__options['g'] + '.*')

        elif key == "WPA-PSK":
            self.stream_edit(self.__options['key'] + '.*', self.__options['key'] + key)
            self.delete(self.__options['algs'] + '.*')
            self.delete(self.__options['wep'] + '.*')
            self.delete(self.__options['wep_txid'] + '.*')
            self.delete(self.__options['eap'] + '.*')
            self.delete(self.__options['phase2'] + '.*')
            self.delete(self.__options['user'] + '.*')
            self.delete(self.__options['pass_key'] + '.*')

        elif key == "WPA-EAP":
            self.stream_edit(self.__options['key'] + '.*', self.__options['key'] + key)
            self.delete(self.__options['algs'] + '.*')
            self.delete(self.__options['wep'] + '.*')
            self.delete(self.__options['wep_txid'] + '.*')
            self.delete(self.__options['p'] + '.*')
            self.delete(self.__options['pair'] + '.*')
            self.delete(self.__options['g'] + '.*')
        else:
            print "Enter correct key_mgt"
        self.stream_edit('^}.*', '}\n')

    def password(self, pwd):
        """Used to set the password to connect to encrypted AP.
        """
        self.delete('^}.*')
        self.stream_edit(self.__options['p'] + '.*', self.__options['p'] + '"' + str(pwd) + '"')
        self.delete(self.__options['algs'] + '.*')
        self.delete(self.__options['wep'] + '.*')
        self.delete(self.__options['wep_txid'] + '.*')
        self.delete(self.__options['eap'] + '.*')
        self.delete(self.__options['phase2'] + '.*')
        self.delete(self.__options['user'] + '.*')
        self.delete(self.__options['pass_key'] + '.*')
        self.stream_edit('^}.*', '}')

    def pairwise(self, *pair):
        """Used to specify the WPA encryption protocol
        """
        self.delete('^}.*')
        self.stream_edit(self.__options['pair'] + '.*', self.__options['pair'] + ' '.join(pair))
        self.delete(self.__options['algs'] + '.*')
        self.delete(self.__options['wep'] + '.*')
        self.delete(self.__options['wep_txid'] + '.*')
        self.stream_edit('^}.*', '}')

    def group(self, *grp):
        """Used to specify the WPA encryption protocol
        """
        self.delete('^}.*')
        self.stream_edit(self.__options['g'] + '.*', self.__options['g'] + ' '.join(grp))
        self.delete(self.__options['algs'] + '.*')
        self.delete(self.__options['wep'] + '.*')
        self.delete(self.__options['wep_txid'] + '.*')
        self.stream_edit('^}.*', '}')

    def wep(self, key, key_no=0):
        """Used to set WEP keys. Can set from 0 - 3 wep keys
        By default, key number will be 0
        """
        self.delete('^}.*')
        if key.isdigit():
            if key_no == 0:
                self.stream_edit(self.__options['wep'] + str(key_no) + '.*',
                                 self.__options['wep'] + str(key_no) + '=' + key)
            if key_no == 1:
                self.stream_edit(self.__options['wep'] + str(key_no) + '.*',
                                 self.__options['wep'] + str(key_no) + '=' + key)
            if key_no == 2:
                self.stream_edit(self.__options['wep'] + str(key_no) + '.*',
                                 self.__options['wep'] + str(key_no) + '=' + key)
            if key_no == 3:
                self.stream_edit(self.__options['wep'] + str(key_no) + '.*',
                                 self.__options['wep'] + str(key_no) + '=' + key)
        else:
            if key_no == 0:
                self.stream_edit(self.__options['wep'] + str(key_no) + '.*',
                                 self.__options['wep'] + str(key_no) + '=' + '"' + key + '"')
            if key_no == 1:
                self.stream_edit(self.__options['wep'] + str(key_no) + '.*',
                                 self.__options['wep'] + str(key_no) + '=' + '"' + key + '"')
            if key_no == 2:
                self.stream_edit(self.__options['wep'] + str(key_no) + '.*',
                                 self.__options['wep'] + str(key_no) + '=' + '"' + key + '"')
            if key_no == 3:
                self.stream_edit(self.__options['wep'] + str(key_no) + '.*',
                                 self.__options['wep'] + str(key_no) + '=' + '"' + key + '"')
        self.delete(self.__options['p'] + '.*')
        self.delete(self.__options['eap'] + '.*')
        self.delete(self.__options['phase2'] + '.*')
        self.delete(self.__options['user'] + '.*')
        self.delete(self.__options['pass_key'] + '.*')
        self.delete(self.__options['pair'] + '.*')
        self.delete(self.__options['g'] + '.*')
        self.stream_edit('^}.*', '}')

    def auth_alg(self):
        """ Used to set the authentication algorithm to shared.
        Only used for WEP authentication mode.
        """
        self.delete('^}.*')
        self.stream_edit(self.__options['algs'] + '.*', self.__options['algs'])
        self.delete(self.__options['p'] + '.*')
        self.delete(self.__options['eap'] + '.*')
        self.delete(self.__options['phase2'] + '.*')
        self.delete(self.__options['user'] + '.*')
        self.delete(self.__options['pass_key'] + '.*')
        self.delete(self.__options['pair'] + '.*')
        self.delete(self.__options['g'] + '.*')
        self.stream_edit('^}.*', '}')

    def wep_default_txid(self, w_def=0):
        """Used to select the default key for WEP encryption. Default key will be `key 0`
        """
        self.delete('^}.*')
        self.stream_edit(self.__options['wep_txid'] + '.*', self.__options['wep_txid'] + str(w_def))
        self.delete(self.__options['p'] + '.*')
        self.delete(self.__options['eap'] + '.*')
        self.delete(self.__options['phase2'] + '.*')
        self.delete(self.__options['user'] + '.*')
        self.delete(self.__options['pass_key'] + '.*')
        self.delete(self.__options['pair'] + '.*')
        self.delete(self.__options['g'] + '.*')
        self.stream_edit('^}.*', '}')

    # @property
    # def iface(self):
    #     """Returns selected wireless interface.
    #     """
    #     return self.__class__._peripheral
    # @iface.setter
    def iface(self, interface):
        """Used to select the wireless interface. By default the interface will be `wlan0`
        """
        self.__class__._peripheral = interface

    def eap_type(self, mode):
        """Used to set the type protocol for eap.
        """
        self.delete('^}.*')
        self.stream_edit(self.__options['eap'] + '.*', self.__options['eap'] + mode)
        self.delete(self.__options['algs'] + '.*')
        self.delete(self.__options['wep'] + '.*')
        self.delete(self.__options['wep_txid'] + '.*')
        self.delete(self.__options['p'] + '.*')
        self.delete(self.__options['pair'] + '.*')
        self.delete(self.__options['g'] + '.*')
        self.stream_edit('^}.*', '}')

    def eap_phase2(self, default="True"):
        """Used to set the authentication phase for MSCHAP.
        """
        self.delete('^}.*')
        if default == "True":
            self.stream_edit(self.__options['phase2'] + '.*', self.__options['phase2'])
            self.delete(self.__options['algs'] + '.*')
            self.delete(self.__options['wep'] + '.*')
            self.delete(self.__options['wep_txid'] + '.*')
            self.delete(self.__options['p'] + '.*')
            self.delete(self.__options['pair'] + '.*')
            self.delete(self.__options['g'] + '.*')
        elif default == "False":
            self.delete('^phase2.*')
            self.delete(self.__options['algs'] + '.*')
            self.delete(self.__options['wep'] + '.*')
            self.delete(self.__options['wep_txid'] + '.*')
            self.delete(self.__options['p'] + '.*')
            self.delete(self.__options['pair'] + '.*')
            self.delete(self.__options['g'] + '.*')
        self.stream_edit('^}.*', '}')

    def user_id(self, name):
        """This will set the username for radius server authentication.
        The given username should present in radius server.
        Otherwise authentication will get failed.
        """
        self.delete('^}.*')
        self.stream_edit(self.__options['user'] + '.*', self.__options['user'] + '"' + name + '"')
        self.delete(self.__options['algs'] + '.*')
        self.delete(self.__options['wep'] + '.*')
        self.delete(self.__options['wep_txid'] + '.*')
        self.delete(self.__options['p'] + '.*')
        self.delete(self.__options['pair'] + '.*')
        self.delete(self.__options['g'] + '.*')
        self.stream_edit('^}.*', '}\n')

    def user_pass(self, key):
        """This will set the password for radius server authentication.
        The password for the given username should match.
        Otherwise authentication should fail.
        """
        self.delete('^}.*')
        self.stream_edit(self.__options['pass_key'] + '.*',
                         self.__options['pass_key'] + '"' + key + '"')
        self.delete(self.__options['algs'] + '.*')
        self.delete(self.__options['wep'] + '.*')
        self.delete(self.__options['wep_txid'] + '.*')
        self.delete(self.__options['p'] + '.*')
        self.delete(self.__options['pair'] + '.*')
        self.delete(self.__options['g'] + '.*')
        self.stream_edit('^}.*', '}\n')

    def serve_sta(self, status):
        """Used to enable and disable the STA
        """
        filename = path.join(self.getpath(), self.name)
        with open(filename, 'r') as conf:
            data = conf.readlines()
        hotspot = 'False'
        self.proxy.board(status, data, hotspot, self._peripheral)

    def __network_block(self):
        """Used to add the network block in config file"""
        with open(self.filename, 'w') as conf:
            conf.write("network={\n}\n")

    def reset(self, default=False):
        """Used to reset the STA configuration to None
        or generate a default STA configuration for new users.
        """
        default = str(default)
        if default == 'False':
            self.delete()
            self.createfile()
            self.__network_block()
        elif default == 'True':
            self.delete()
            self.createfile()
            self.__network_block()
            self.ssid('AccessPoint')
            self.key_mgt('WPA-PSK')
            self.password('12345678')

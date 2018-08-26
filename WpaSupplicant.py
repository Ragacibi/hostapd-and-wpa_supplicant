"""This module is used to configure the wpa supplicant """
from os import path
from xmlrpclib import ServerProxy
from ConfFile import ConfFile


class WpaSupplicant(ConfFile):
    """Class WpaSupplicant
    Example:- Open
    ----------
    | ssid | QA-AP |
    | key mgt | NONE |
    -----------

    Example:- WEP-SHARED
    ------
    | ssid | QA-AP
    | key mgt | NONE |
    | wep | 123456 | 0 |
    | wep |145adcf | 1 |
    | wep default txid | 1
    | auth alg |
    ---------

    Example:- WPA-PSK / WPA2-PSK
    ----------
    | ssid | QA-AP |
    | key mgt | WPA-PSK |
    | password | 1234567 |
    | pairwise | TKIP | CCMP |
    | group    | TKIP | CCMP |
    -----------

    Example:- Radius-Server
    ---------
    | ssid | QA-AP |
    | key mgt | WPA-EAP |
    | eap type | TTLS    |
    | user id  | user    |
    | user pass| 1234567 |
    -----------


    """
    # Attributes:

    peripheral = 'wlan0'
    
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
                 'g':'group='
                 }
    
    # Operations
    def __init__(self, name, server_ip, server_port=80):
        """Generates a configuration file.

        `name` specifies the name of the configuration file.

        Example:
        -------
        | ** Settings** | *Arguments* |
        | Library       | name        | server ip |
        ------
        """
        ConfFile.__init__(self, name)
        self.proxy = ServerProxy("http://" + str(server_ip) + ":" + str(server_port), allow_none=False)

    def ssid(self, nw_name):
        """Used to connect the station to the ssid given.
        Example:
        ----
        | ssid | Testing-AP |
        -----
        """
        self.delete('^}.*')
        self.stream_edit(self.__options['s'] + '.*', self.__options['s'] + '"' + nw_name + '"')
        self.stream_edit('^}.*', '}\n')

    def key_mgt(self, key='WPA-PSK'):
        """Used to select the WPA security
        By default, the security will be WPA-PSK
        Example:
        -------
        | key_mgt | WPA-PSK | #For WPA and WPA2 |
        | key_mgt | NONE    | #No Security      |
        | key_mgt | WEP     | #For WEP Shared   |
        -------
        Values to the keyword are case sensitive
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
            print "entered wpa-psk"
            self.stream_edit(self.__options['key'] + '.*', self.__options['key'] + key)
            print("hi")
            self.delete(self.__options['algs'] + '.*')
            print("hi")
            self.delete(self.__options['wep'] + '.*')
            print("hi")
            self.delete(self.__options['wep_txid'] + '.*')
            print("hi")
            self.delete(self.__options['eap'] + '.*')
            print("hi")
            self.delete(self.__options['phase2'] + '.*')
            print("hi")
            self.delete(self.__options['user'] + '.*')
            print("hi")
            self.delete(self.__options['pass_key'] + '.*')
            print("hi")

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
        Example:
        ------
        | password | 123456 |
        -------
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
        Example:
        ----
        | pairwise | CCMP |      |
        | pairwise | CCMP | TKIP |
        ----
        """
        self.delete('^}.*')
        self.stream_edit(self.__options['pair'] + '.*', self.__options['pair'] + ' '.join(pair))
        self.delete(self.__options['algs'] + '.*')
        self.delete(self.__options['wep'] + '.*')
        self.delete(self.__options['wep_txid'] + '.*')
        self.delete(self.__options['eap'] + '.*')
        self.delete(self.__options['phase2'] + '.*')
        self.delete(self.__options['user'] + '.*')
        self.delete(self.__options['pass_key'] + '.*')
        self.stream_edit('^}.*', '}')

    def group(self, *grp):
        """Used to specify the WPA encryption protocol
        Example:
        ----
        | group | TKIP |      |
        | group | TKIP | CCMP | WEP104 | WEP40 |
        ----
        """
        self.delete('^}.*')
        self.stream_edit(self.__options['g'] + '.*', self.__options['g'] + ' '.join(grp))
        self.delete(self.__options['algs'] + '.*')
        self.delete(self.__options['wep'] + '.*')
        self.delete(self.__options['wep_txid'] + '.*')
        self.delete(self.__options['eap'] + '.*')
        self.delete(self.__options['phase2'] + '.*')
        self.delete(self.__options['user'] + '.*')
        self.delete(self.__options['pass_key'] + '.*')
        self.stream_edit('^}.*', '}')

    def wep(self, key, key_no=0):
        """Used to set WEP keys
        Can set from 0 - 3 wep keys
        Example:
        ----
        | wep | 3CB2AB7CDE | 0 |
        | wep | FDABE42844 | 1 |
        ----
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
        Example:
        ------
        | auth alg |
        ------
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
        """Used to select the default key for WEP encryption
        Example:
        ----
        | wep default txid | 3 |
        ----
        Default key will be `key 0`
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

    def iface(self, interface):
        """Used to select the wireless interface
        By default the interface will be `wlan0`
        ----
        Example:
        | iface | wlan0 |
        ----
        """
        self.peripheral = interface

    def eap_type(self, mode):
        """Used to set the type protocol for eap.
        Example:
        --------
        | eap type | TTLS |
        | eap type | PEAP |
        --------
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
        Example:
        ------
        | eap phase2 | True  |
        | eap phase2 | False |
        -----
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
        Example:
        ------
        | user id | username |
        ------
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
        Example:
        -----
        | user pass | password |
        -----
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
        Example:
        ------
        | serve sta | start | #Starts the STA |
        | serve sta | stop  | #Stops the STA  |
        -----
        The Values to the keyword are case sensitive
        """
        filename = path.join(self.getpath(), self.name)
        with open(filename, 'r') as conf:
            data = conf.readlines()
        hotspot = 'False'
        print "Before"
        print self.peripheral
        print type(status)
        print type(data)
        print type(hotspot)
        
        self.proxy.board(status, data, hotspot, self.peripheral)
        print "After"

    def __network_block(self):
        """Used to add the network block in config file"""
        with open(self.filename, 'w') as conf:
            conf.write("network={\n}\n")

    def reset(self, default=False):
        """Used to reset the STA configuration to None
        or generate a default STA configuration for new users.
        Example:
        ------
        | reset |              | #resets the configuration to None |
        | reset | default=True | #generates default configuration  |
        -----
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

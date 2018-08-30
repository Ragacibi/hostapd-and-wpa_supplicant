'''Python module to configure AP using hostpad'''

from os import path
from xmlrpclib import ServerProxy
from ConfFile import ConfFile


class Hostapd(ConfFile):
    """Class Hostapd to configure hostapd
    """
    # Attributes:
    __options = {'a':"auth_algs=",
                 'b':"beacon_int=",
                 'c':"channel=",
                 'd':"driver=",
                 'h':"hw_mode=",
                 'i':"interface=",
                 'k':"wpa_key_mgmt=",
                 'm':"ieee80211",
                 'n':"country_code=",
                 's':"ssid=",
                 't':"basic_rates=",
                 'u':"supported_rates=",
                 'w':"wpa_passphrase=",
                 'y':"wpa_pairwise=",
                 'z':"rsn_pairwise=",
                 'wpa':"wpa=",
                 'wep_def':"wep_default_key=",
                 'key':'wep_key',
                 'x':'ieee8021x=',
                 'asa':'auth_server_addr=',
                 'asp':'auth_server_port=',
                 'ass':'auth_server_shared_secret=',
                 'msg':'eap_message=',
                 'ht_capab':'ht_capab=',
                 'wmm':'wmm_enabled=',
                 'ctrl_iface':'ctrl_interface=',
                 'ctrl_iface_grp':'ctrl_interface_group=',
                }

    # Operations
    def __init__(self, name, server_ip, server_port='80'):
        """Generates a configuration file.
        `name` specifies the name of the configuration file.
        """
        ConfFile.__init__(self, name)
        self.proxy = ServerProxy("http://" + server_ip + ":" + server_port, allow_none=False)

    def auth_algs(self, auth):
        """Used to specify authentication algorithm
        """
        self.stream_edit(self.__options['a'] + '.*', self.__options['a'] + auth)

    def beacon_interval(self, b_int):
        """Used to set the beacon interval of AP
        """
        self.stream_edit(self.__options['b'] + '.*', self.__options['b'] + b_int)

    def channel(self, chan):
        """Used to specify the operating channel of AP
        """
        self.stream_edit(self.__options['c'] + '.*', self.__options['c'] + str(chan))

    def ap_ctrl_interface(self, ctrl_iface_ap):
        """Used to set the control interface of AP
        """
        self.stream_edit(self.__options['ctrl_iface'] + '.*', self.__options['ctrl_iface'] + ctrl_iface_ap)

    def ap_ctrl_interface_group(self, ctrl_iface_grp_ap):
        """Used to set the control interface of AP
        """
        self.stream_edit(self.__options['ctrl_iface_grp'] + '.*', self.__options['ctrl_iface_grp'] + ctrl_iface_grp_ap)

    def driver(self, driv):
        """To sepcify driver
        """
        self.stream_edit(self.__options['d'] + '.*', self.__options['d'] + driv)

    def interface(self, iface='wlan0'):
        """Used to select the wireless interface
        By default the interface will be `wlan0`
        """
        self.stream_edit(self.__options['i'] + '.*', self.__options['i'] + iface)

    def mode(self, std):
        """"Used to select operating mode
        """
        n2g = ['n', 'n2.4', 'n2.4G', 'n2.4GHz']
        n5g = ['n5', 'n5G', 'n5GHz']

        if std == 'a' or std == 'b' or std == 'g':
            self.stream_edit(self.__options['h'] + '.*', self.__options['h'] + std)

        if std in n2g:
            self.stream_edit(self.__options['h'] + '.*', self.__options['h'] + 'g')
            self.stream_edit(self.__options['m'] + '.*', self.__options['m'] + 'n=1')

        if std in n5g:
            self.stream_edit(self.__options['h'] + '.*', self.__options['h'] + 'a')
            self.stream_edit(self.__options['m'] + '.*', self.__options['m'] + 'n=1')

        if std == 'ac':
            self.stream_edit(self.__options['h'] + '.*', self.__options['h'] + 'a')
            self.stream_edit(self.__options['m'] + '.*', self.__options['m'] + 'ac=1')

        self.delete(self.__options['t'] + '.*')
        self.delete(self.__options['u'] + '.*')
        self.delete(self.__options['wmm'] + '.*')

    def country_code(self, nation='IN'):
        """Used to set country of operation of AP
        By default the coutry of operation is India (IN).
        """
        nation = nation.upper()
        self.stream_edit(self.__options['n'] + '.*', self.__options['n'] + nation)

    def ap_ssid(self, nw_name):
        """Used to provide ssid for the AP.
        """
        self.stream_edit(self.__options['s'] + '.*', self.__options['s'] + nw_name)

    def wpa_key_mgmt(self, wpa_key='WPA2-PSK'):
        """Used to select the WPA security
        By default, the security will be WPA2-PSK.
        """
        wpa_key = wpa_key.upper()
        if wpa_key == 'NONE':
            self.delete(self.__options['k'] + '.*')
            self.delete(self.__options['w'] + '.*')
            self.delete(self.__options['y'] + '.*')
            self.delete(self.__options['z'] + '.*')
            self.delete(self.__options['wpa'] + '.*')
            self.delete(self.__options['x'] + '.*')
            self.delete(self.__options['asa'] + '.*')
            self.delete(self.__options['asp'] + '.*')
            self.delete(self.__options['ass'] + '.*')
            self.delete(self.__options['msg'] + '.*')
        if wpa_key == 'WPA-PSK':
            self.stream_edit(self.__options['wpa'] + '.*', self.__options['wpa'] + '1')
            self.stream_edit(self.__options['k'] + '.*', self.__options['k'] + 'WPA-PSK')
            self.delete(self.__options['x'] + '.*')
            self.delete(self.__options['asa'] + '.*')
            self.delete(self.__options['asp'] + '.*')
            self.delete(self.__options['ass'] + '.*')
            self.delete(self.__options['msg'] + '.*')
        if wpa_key == 'WPA2-PSK':
            self.stream_edit(self.__options['wpa'] + '.*', self.__options['wpa'] + '2')
            self.stream_edit(self.__options['k'] + '.*', self.__options['k'] + 'WPA-PSK')
            self.delete(self.__options['x'] + '.*')
            self.delete(self.__options['asa'] + '.*')
            self.delete(self.__options['asp'] + '.*')
            self.delete(self.__options['ass'] + '.*')
            self.delete(self.__options['msg'] + '.*')
        if wpa_key == 'WPA/WPA2-PSK':
            self.stream_edit(self.__options['wpa'] + '.*', self.__options['wpa'] + '3')
            self.stream_edit(self.__options['k'] + '.*', self.__options['k'] + 'WPA-PSK')
            self.delete(self.__options['x'] + '.*')
            self.delete(self.__options['asa'] + '.*')
            self.delete(self.__options['asp'] + '.*')
            self.delete(self.__options['ass'] + '.*')
            self.delete(self.__options['msg'] + '.*')
        if wpa_key == 'WPA-Radius':
            self.stream_edit(self.__options['x'] + '.*', self.__options['x'] + '1')
            self.stream_edit(self.__options['wpa'] + '.*', self.__options['wpa'] + '1')
            self.stream_edit(self.__options['k'] + '.*', self.__options['k'] + 'WPA-EAP')
        if wpa_key == 'WPA2-Radius':
            self.stream_edit(self.__options['x'] + '.*', self.__options['x'] + '1')
            self.stream_edit(self.__options['wpa'] + '.*', self.__options['wpa'] + '2')
            self.stream_edit(self.__options['k'] + '.*', self.__options['k'] + 'WPA-EAP')
        if wpa_key == 'WPA/WPA2-Radius':
            self.stream_edit(self.__options['x'] + '.*', self.__options['x'] + '1')
            self.stream_edit(self.__options['wpa'] + '.*', self.__options['wpa'] + '3')
            self.stream_edit(self.__options['k'] + '.*', self.__options['k'] + 'WPA-EAP')
        self.delete(self.__options['wep_def'] + '.*')
        self.delete(self.__options['key'] + '.*')

    def auth_server(ip, port):
        '''Used to Set Radius Server address and port
        '''
        self.stream_edit(self.__options['asa'] + '.*', self.__options['asa'] + str(ip))
        self.stream_edit(self.__options['asp'] + '.*', self.__options['asp'] + str(port))

    def auth_server_secret(shared_secret):
        '''Used to Set Radius Server password
        '''
        self.stream_edit(self.__options['ass'] + '.*', self.__options['ass'] + str(shared_secret))

    def eap_msg(msg):
        '''Used to customize Radius server's message
        '''
        self.stream_edit(self.__options['msg'] + '.*', self.__options['msg'] + msg)

    def wpa_passphrase(self, wpa_pass):
        """Used to set the password when any one of WPA mechanism is used.
        """
        self.stream_edit(self.__options['w'] + '.*', self.__options['w'] + wpa_pass)

    def basic_rates(self, *br):
        """"Used to set basic rates for AP
        Values to the keyword can be a list
        """
        self.stream_edit(self.__options['t'] + '.*', self.__options['t'] + ' '.join(br))

    def supported_rates(self, *sr):
        """"Used to set supported rates for AP
        Values to the keyword can be a list
        """
        self.stream_edit(self.__options['u'] + '.*', self.__options['u'] + ' '.join(sr))

    def ht_capabilities(self, *capab):
        """Used to set HT Capabilities of AP
        """
        ht = ''
        for _ in capab:
            ht += '[{}]'.format(_)
        self.stream_edit(self.__options['ht_capab'] + '.*', self.__options['ht_capab'] + ht)

    def wpa_pairwise(self, *w_pair):
        """Used to specify the WPA encryption protocol
        """
        self.stream_edit(self.__options['y'] + '.*', self.__options['y'] + ' '.join(w_pair))

    def rsn_pairwise(self, r_pair):
        """Used to specify the RSN encryption protocol
        """
        self.stream_edit(self.__options['z'] + '.*', self.__options['z'] + r_pair)

    def wep_default_key(self, w_def=0):
        """Used to select the default key for WEP encryption
        Default key will be `key 0`
        """
        self.stream_edit(self.__options['wep_def'] + '.*', self.__options['wep_def'] + str(w_def))

    def wep_key(self, key, key_no=0):
        """Used to set WEP keys. Can set from 0 - 3 wep keys
        By default, key number will be 0
        """
        if key_no == '0':
            self.stream_edit(self.__options['key'] + str(key_no) + '.*', self.__options['key'] + str(key_no)  + '=' + key)
        if key_no == '1':
            self.stream_edit(self.__options['key'] + str(key_no) + '.*', self.__options['key'] + str(key_no) + '=' + key)
        if key_no == '2':
            self.stream_edit(self.__options['key'] + str(key_no) + '.*', self.__options['key'] + str(key_no) + '=' + key)
        if key_no == '3':
            self.stream_edit(self.__options['key'] + str(key_no) + '.*', self.__options['key'] + str(key_no) + '=' + key)
        self.delete(self.__options['k'] + '.*')
        self.delete(self.__options['w'] + '.*')
        self.delete(self.__options['y'] + '.*')
        self.delete(self.__options['z'] + '.*')
        self.delete(self.__options['wpa'] + '.*')
        self.delete(self.__options['x'] + '.*')
        self.delete(self.__options['asa'] + '.*')
        self.delete(self.__options['asp'] + '.*')
        self.delete(self.__options['ass'] + '.*')
        self.delete(self.__options['msg'] + '.*')

    def serve_ap(self, status):
        """Used to enable and disable the AP
        """
        status = status.lower()
        filename = path.join(self.getpath(), self.name)
        with open(filename, 'r') as conf:
            data = conf.readlines()
        hotspot = 'True'
        iface = ''
        self.proxy.board(status, data, hotspot, iface)

    def is_connected(self, sta_mac=''):
        """Used to verify whether the station and AP are connected
        """
        c_mac = self.proxy.verify_connection()
        if sta_mac in c_mac:
            pass
        else:
            raise Exception("Station is not connected")

    def reset_conf(self, default=False):
        """Used to reset the AP configuration to None or generate a default AP configuration for new users.
        """
        default = bool(default)
        if not default:
            self.delete()
        if default:
            self.delete()
            self.wpa_passphrase('12345678')
            self.interface('wlan0')
            self.driver('nl80211')
            self.ap_ssid('AccessPoint')
            self.channel(1)
            self.mode('g')
            self.wpa_key_mgmt('WPA2-PSK')
            self.wpa_pairwise('CCMP')
            self.rsn_pairwise('CCMP')

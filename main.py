import subprocess
import app

def start_access_point():
    ssid = "RaspberryPiAccessPoint"
    password = "1234ABCD"
    ap_config = f"""interface=wlan0
driver=nl80211
ssid={ssid}
hw_mode=a
channel=36
ieee80211n=1
ieee80211ac=1
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase={password}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
"""

    with open("/etc/hostapd/hostapd.conf", "w") as f:
        f.write(ap_config)

    # update hostapd default configuration
    hostapd_default = "/etc/default/hostapd"
    with open(hostapd_default, "r") as f:
        content = f.read()
    with open(hostapd_default, "w") as f:
        content = content.replace("#DAEMON_CONF=\"\"", f'DAEMON_CONF="/etc/hostapd/hostapd.conf"')
        f.write(content)

    # configure dnsmasq
    eth0_config = """\ninterface eth0
static ip_address=192.168.1.1/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1
"""

    wlan0_config = """\ninterface wlan0
static ip_address=192.168.0.50/24
nohook wpa_supplicant
"""

    with open("/etc/dhcpcd.conf", "w") as f:
	    f.write(eth0_config)
	    f.write(wlan0_config)


    with open("/etc/dnsmasq.conf", "w") as f:
        f.write("\ninterface=wlan0\nlisten-address=192.168.0.50\nserver=8.8.8.8\ndomain-needed\nbogus-priv\ndhcp-range=192.168.0.50,192.168.0.70,12h\n")

    subprocess.call(["sudo", "systemctl", "unmask", "hostapd"])
    subprocess.call(["sudo", "systemctl", "unmask", "dhcpcd"])
    subprocess.call(["sudo", "systemctl", "enable", "hostapd"])
    subprocess.call(["sudo", "systemctl", "enable", "dhcpcd"])
    subprocess.call(["sudo", "systemctl", "start", "hostapd"])
    subprocess.call(["sudo", "systemctl", "enable", "dnsmasq"])
    subprocess.call(["sudo", "systemctl", "restart", "dhcpcd"])
    subprocess.call(["sudo", "systemctl", "restart", "dnsmasq"])
    subprocess.call(["sudo", "systemctl", "restart", "hostapd"])

if __name__ == "__main__":
    start_access_point()
    app.start()

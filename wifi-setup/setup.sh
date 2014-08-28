#!/bin/sh

INTERFACES="/etc/network/interfaces"
WPA="/etc/wpa_supplicant/wpa_supplicant.conf"


echo "Please enter your WiFi SSID: "
read ssid
echo "Please enter your password:"
read psk

/bin/cat <<EOM >$INTERFACES
auto wlan0
iface lo inet loopback
iface eth0 inet dhcp
allow-hotplug wlan0
iface wlan0 inet dhcp
wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet dhcp
EOM

/bin/cat <<EOM >$WPA
# /etc/wpa_supplicant/wpa_supplicant.conf
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
ssid="$ssid"
psk="$psk"
proto=RSN
key_mgmt=WPA-PSK
pairwise=CCMP
auth_alg=OPEN
}
EOM
export WIFINAME=$ssid


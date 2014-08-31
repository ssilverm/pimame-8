#!/bin/sh

INTERFACES="/etc/network/interfaces"
WPA="/etc/wpa_supplicant/wpa_supplicant.conf"


echo "Please enter your WiFi SSID: "
read ssid
echo "Please enter your password:"
read psk
echo "Please enter your encryption protocol - TKIP or CCMP:"
echo "Generally CCMP is WPA2 and TKIP is WPA1. If in doubt, try TKIP first."
read encryption
echo "Please enter the protocol - RSN or WPA:"
echo "Could be either RSN (WPA2) or WPA (WPA1)"
read proto

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
proto=$proto
key_mgmt=WPA-PSK
pairwise=$encryption
auth_alg=OPEN
}
EOM
export WIFINAME=$ssid

echo "WiFi Successfully Setup! Reboot to test changes."


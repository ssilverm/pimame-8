#!/bin/bash
if grep --quiet 'xboxdrv' /home/pi/.profile; then
  echo "xboxdrv already exists, removing."
  #sed -i '/sudo xboxdrv --silent --config /home/pi/pimame_files/xboxdrv_mapping.cfg --dbus session &/d' /home/pi/.profile
  grep -v "xboxdrv" /home/pi/.profile > profile.temp && rm /home/pi/.profile && mv profile.temp /home/pi/.profile
else
  echo "Activating Xboxdrv.  Please restart"
  LINE=$(awk '/launchmenu/{print NR}' /home/pi/.profile)
  echo $LINE
  LINE=$((LINE-1))
  echo $LINE
  #sed '{$LINE}isudo xboxdrv --silent --config /home/pi/pimame/config/xboxdrv_mapping.cfg --dbus session &' /home/pi/.profile
  awk -v n=$LINE -v s="sudo xboxdrv --silent --config /home/pi/pimame/config/xboxdrv_mapping.cfg --dbus session &" 'NR == n {print s} {print}' /home/pi/.profile > profile.temp && rm /home/pi/.profile && mv profile.temp /home/pi/.profile
  #echo 'sudo xboxdrv --silent --config /home/pi/pimame/config/xboxdrv_mapping.cfg --dbus session &' >> /home/pi/.profile
fi

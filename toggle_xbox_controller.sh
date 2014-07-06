#!/bin/bash
if grep --quiet xboxdrv /home/pi/.profile; then
  echo "xboxdrv already exists, removing."
  sed -i '/sudo xboxdrv --silent --config /home/pi/pimame_files/xboxdrv_mapping.cfg --dbus session &/d' /home/pi/.profile
else
  echo "Activating Xboxdrv.  Please restart"
  echo 'sudo xboxdrv --silent --config /home/pi/pimame/config/xboxdrv_mapping.cfg --dbus session &' >> /home/pi/.profile
fi

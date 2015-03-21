# Import the module
import subprocess
import sys
import requests
import sqlite3

def connected_to_internet(url='http://piplay.org/', timeout=5):
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
    return False

connection = connected_to_internet();

if connection:
    print "Connection Established"
else:
    print "Could not connect to the internet/piplay.org"
    sys.exit()

print "Downloading and Installing MAME"

download_and_install = '''
####MAME START#####
cd /home/pi/pimame
wget http://sheasilverman.com/rpi/raspbian/debs/advancemame-raspberrypi_1-1_armhf.deb
wget http://sheasilverman.com/rpi/raspbian/debs/advancemenu_2.6-1_armhf.deb
wget http://sheasilverman.com/rpi/raspbian/debs/advancemess_0.102.0.1-1_armhf.deb
sudo dpkg --force-overwrite -i advancemenu_2.6-1_armhf.deb 
sudo dpkg --force-overwrite -i advancemame-raspberrypi_1-1_armhf.deb
sudo dpkg --force-overwrite -i advancemess_0.102.0.1-1_armhf.deb
rm advancemame-raspberrypi_1-1_armhf.deb 
rm advancemenu_2.6-1_armhf.deb 
rm advancemess_0.102.0.1-1_armhf.deb

###mame4all
cd /home/pi/pimame/emulators/
git clone https://github.com/ssilverm/mame4all_pi-piplay mame4all-pi
cd mame4all-pi
rm -rf ./roms
ln -s /home/pi/pimame/roms/mame4all/ roms
cd /home/pi/pimame

####MAME END#########
cd /home/pi/pimame/pimame-menu/
'''

# Set up the echo command and direct the output to a pipe
subprocess.call(download_and_install, shell=True)

print "Updating PiPlay Database"
conn = sqlite3.connect('/home/pi/pimame/pimame-menu/database/config.db')
c = conn.cursor()

c.execute('UPDATE menu_items SET visible = 1 where icon_id = "M4A" OR icon_id = "ADVM"')
c.execute('UPDATE menu_items SET visible = 0 where icon_id = "INSTALLMAME"')
conn.commit()



print "All Finished!"

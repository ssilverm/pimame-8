# Import the module
import subprocess
import sys
import requests

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
#wget http://sheasilverman.com/rpi/raspbian/debs/advancemame_1.2-1_armhf.deb
wget http://sheasilverman.com/rpi/raspbian/debs/advancemame-raspberrypi_1-1_armhf.deb
wget http://sheasilverman.com/rpi/raspbian/debs/advancemenu_2.6-1_armhf.deb
wget http://sheasilverman.com/rpi/raspbian/debs/advancemess_0.102.0.1-1_armhf.deb
sudo dpkg --force-overwrite -i advancemenu_2.6-1_armhf.deb 
sudo dpkg --force-overwrite -i advancemame-raspberrypi_1-1_armhf.deb
sudo dpkg --force-overwrite -i advancemess_0.102.0.1-1_armhf.deb
rm advancemame-raspberrypi_1-1_armhf.deb 
rm advancemenu_2.6-1_armhf.deb 
rm advancemess_0.102.0.1-1_armhf.deb
#rm advancemame_1.2-1_armhf.deb

###mame4all
cd /home/pi/pimame
git clone https://code.google.com/p/mame4all-pi/
mkdir /home/pi/pimame/emulators/mame4all-pi/
cp mame4all-pi/mame4all_pi.zip /home/pi/pimame/emulators/mame4all-pi/
cd /home/pi/pimame/emulators/mame4all-pi/
unzip -o mame4all_pi.zip
cd /home/pi/pimame
rm -rf mame4all-pi/

####MAME END#########
cd /home/pi/pimame/pimame-menu/
'''

# Set up the echo command and direct the output to a pipe
subprocess.call(download_and_install, shell=True)

print "Updating PiPlay Configuration File"
f = open('/home/pi/pimame/pimame-menu/config.yaml', 'r')
config_file = f.readlines()

#print config_file
found_lines = []
count = 0
for x in config_file:
    if "AdvMAME" in x:
        found_lines.append(count)
    if "MAME4All" in x:
        found_lines.append(count)
    if "Install MAME" in x:
        found_lines.append(count)
    count += 1

#print found_lines, count

for x in found_lines:
    if "visible" in config_file[x + 1]:
        if "No" in config_file[x + 1]: 
            print "Making Item Visible"
            config_file[x + 1] = config_file[x + 1].replace("No","Yes")
        elif "Yes" in config_file[x + 1]: 
            print "Making Item Invisible"
            config_file[x + 1] = config_file[x + 1].replace("Yes","No")

f = open('/home/pi/pimame/pimame-menu/config.yaml', 'w')
for item in config_file:
    f.write("%s" % item)

print "All Finished!"


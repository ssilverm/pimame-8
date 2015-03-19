# file_watcher
-sudo pip install watchdog

-python watch /home/pi/pimame/roms

program will watch roms folder. When a new file is created or deleted,
the program will add that folder to the scrape list. If the scrape list
contains changes, then it will run the scraper automatically every 60
seconds.

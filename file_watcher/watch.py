import sys
import time
import os
import logging
import sqlite3
from watchdog.observers import Observer
#from watchdog.events import LoggingEventHandler
from watchdog.events import PatternMatchingEventHandler
import argparse

parser = argparse.ArgumentParser(description='PiScraper')
parser.add_argument("--delay", default=60, metavar="60", help="How long to wait before running scraper", type=int)
parser.add_argument("--path", default='.', metavar="/path/to/watch", help="folder to monitor", type=str)

args = parser.parse_args()


class EventHandler(PatternMatchingEventHandler):
    info = []
    def on_any_event(self, event):

        if not event.is_directory:
            self.conn = sqlite3.connect('/home/pi/pimame/pimame-menu/database/config.db')
            self.c = self.conn.cursor()
            if event.event_type == 'created': 
                self.info.append(self.c.execute('SELECT id FROM menu_items WHERE rom_path LIKE "{0}%"'.format(os.path.dirname(event.src_path))).fetchone()[0])
                print 'new file found:', event.src_path
            if event.event_type == 'deleted':
                self.info.append(self.c.execute('SELECT id FROM menu_items WHERE rom_path LIKE "{0}%"'.format(os.path.dirname(event.src_path))).fetchone()[0])
                print 'file deleted:', event.src_path
	else: print

if __name__ == "__main__":
    path = args.path
    event_handler = EventHandler(ignore_patterns=['*.jpg', '*.png', '*.gif', '*.gitkeep'], case_sensitive=False)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(args.delay)
            if event_handler.info: os.system('python /home/pi/pimame/pimame-menu/scraper/scrape_script.py --platform {0}'.format(str(set(event_handler.info))[5:-2].replace(' ','')))
            event_handler.info = []
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


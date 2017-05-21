#!/usr/bin/python

import time
import threading
import pyperclip
import daemon


def is_dropbox_link(clipboard_content):
	if clipboard_content.startswith("https://") and "www.dropbox.com" in clipboard_content and "dl=0" in clipboard_content:
		return True
	return False

def make_dl_link(url):
	pyperclip.copy(url.replace("www", "dl"))

class ClipboardWatcher(threading.Thread):
	def __init__(self, predicate, callback, pause=5.):
		super(ClipboardWatcher, self).__init__()
		self._predicate = predicate
		self._callback = callback
		self._pause = pause
		self._stopping = False

	def run(self):
		recent_value = ""
		while not self._stopping:
			tmp_value = pyperclip.paste()
			if tmp_value != recent_value:
				recent_value = tmp_value
				if self._predicate(recent_value):
					self._callback(recent_value)
			time.sleep(self._pause)

	def stop(self):
		self._stopping = True

def watch_clipboard():
	watcher = ClipboardWatcher(is_dropbox_link,
							   make_dl_link,
							   pause=5)
	watcher.start()
	while True:
		try:
			time.sleep(10)
		except KeyboardInterrupt:
			watcher.stop()
			break

	
def main():
	with daemon.DaemonContext():
		watch_clipboard()

if __name__ == "__main__":
	main()
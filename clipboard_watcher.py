#!/usr/bin/python

import time
import threading
import pyperclip


def is_dropbox_link(clipboard_content):
	if clipboard_content.startswith("https://") and "www.dropbox.com" in clipboard_content and "dl=0" in clipboard_content:
		return True
	return False

def make_dl_link(url):
	pyperclip.copy(url.replace("www", "dl"))

class ClipboardWatcher(threading.Thread):
	def __init__(self, predicate, callback, num, pause=5.):
		super(ClipboardWatcher, self).__init__()
		self._predicate = predicate
		self._callback = callback
		self._pause = pause
		self._stopping = False
		self.num=num
		print("ClipboardWatcher " + str(self.num) + " starting")

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
		print("ClipboardWatcher " + str(self.num) + " stopping")


def watch_clipboard():
	watchers = []
	for i in range(0, 10):
		new_watcher = ClipboardWatcher(is_dropbox_link,
							   make_dl_link,num=i,
							   pause=5)
		watchers.append(new_watcher)
		new_watcher.start()
		
	while True:
		try:
			time.sleep(10)
		except KeyboardInterrupt:
			for watcher in watchers:
				watcher.stop()
			break

	
def main():
	watch_clipboard()

if __name__ == "__main__":
	main()
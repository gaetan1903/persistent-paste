import sys
from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '360')
#--------------------------
from kivy.lang import Builder 
from kivymd.app import MDApp
#--------------------------

from pynput import keyboard
from pynput.keyboard import Key, Controller
from threading import Thread
import pyperclip


# Le combinaison a voir
COMBINATION = {keyboard.Key.cmd, keyboard.Key.shift}

current = set()
clavier = Controller()
_listener = None


class Ecoute(Thread):
	def run(self):
		with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
			global _listener
			_listener = listener
			listener.join()


def on_press(key):
    if key in COMBINATION:
        current.add(key)
        if all(k in current for k in COMBINATION):
            print('All modifiers active!')
            pyperclip.paste()


def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass


ecoute = Ecoute()
ecoute.start()


_ecoute = ""


class PersistentPASS(MDApp):
    def __init__(self):
    	MDApp.__init__(self)
    	with open('gui.kv', encoding='utf-8') as f:
            self.GUI = Builder.load_string(f.read())

    def build(self):
    	self.theme_cls.primary_palette = "Teal"
    	return self.GUI


    def save(self):
    	pyperclip.copy(self.GUI.ids.paste.text)


    def on_request_close(self, *args):
    	if _listener:
    		_listener.stop()
    	sys.exit(1)


PersistentPASS().run()
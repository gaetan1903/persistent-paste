import os, sys, pickle, signal
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

# Le combinaison a voir
COMBINATION = {keyboard.Key.cmd, keyboard.Key.shift}

current = set()
clavier = Controller()
_listener = None
_ecoute = ""



class Ecoute(Thread):
    def __init__(self):
        Thread.__init__(self)


    def run(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as self.listener:
            self.listener.join()


    def on_press(self, key):
        if key in COMBINATION:
            current.add(key)
            if all(k in current for k in COMBINATION):
                print('All modifiers active!')
                global _ecoute
                clavier.type(_ecoute)


    def on_release(self, key):
        try:
            current.remove(key)
        except KeyError:
            pass



class PersistentPASS(MDApp):
    def __init__(self):
    	MDApp.__init__(self)
    	with open('gui.kv', encoding='utf-8') as f:
            self.GUI = Builder.load_string(f.read())


    def build(self):
    	self.theme_cls.primary_palette = "Teal"
    	return self.GUI


    def save(self):
        global _ecoute
        _ecoute = self.GUI.ids.paste.text


    def on_request_close(self, *args):
        ecoute.listener.stop()
        sys.exit(1)



def getPid():
    if os.path.isfile('__pid'):
        with open('__pid', 'rb') as _pid:
            pid = pickle.load(_pid)
        os.kill(pid, signal.SIGSTOP)


def setPid():
    with open('__pid', 'wb') as _pid:
        pickle.dump(os.getpid(), _pid)




if __name__ == '__main__':
    getPid()
    setPid()
    ecoute = Ecoute()
    ecoute.start()
    PersistentPASS().run()
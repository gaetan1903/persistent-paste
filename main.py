from kivy.lang import Builder
from threading import Thread
from pynput.keyboard import Key, Controller
from pynput import keyboard
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
import os
import sys
import pickle
import signal
from kivy.config import Config

from utils import translate
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '660')
Config.set('graphics', 'height', '460')
# --------------------------
# --------------------------


# Le combinaison a voir
COMBINATION = [
    {keyboard.Key.ctrl, keyboard.Key.shift, keyboard.KeyCode.from_char('1')},
    {keyboard.Key.ctrl, keyboard.Key.shift, keyboard.KeyCode.from_char('2')},
    {keyboard.Key.ctrl, keyboard.Key.shift, keyboard.KeyCode.from_char('3')},
]

current = set()
clavier = Controller()
_listener = None
_ecoute = ["", "", ""]


class Ecoute(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as self.listener:
            self.listener.join()

    def on_press(self, key):

        if key in COMBINATION[0]:
            current.add(key)
            if all(k in current for k in COMBINATION[0]):
                clavier.type(_ecoute[0])

        elif key in COMBINATION[1]:
            current.add(key)
            if all(k in current for k in COMBINATION[1]):
                clavier.type(_ecoute[1])

        elif key in COMBINATION[2]:
            current.add(key)
            if all(k in current for k in COMBINATION[2]):
                clavier.type(_ecoute[2])

    def on_release(self, key):
        try:
            current.remove(key)
        except KeyError:
            pass


class PersistentPASTE(MDApp):

    def __init__(self):
        MDApp.__init__(self)
        self.lang = 'en'
        with open('gui.kv', encoding='utf-8') as f:
            self.GUI = Builder.load_string(f.read())

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        return self.GUI

    def save(self):
        global _ecoute

        for i in range(3):
            _ecoute[i] = self.GUI.ids[f'paste_{i+1}'].text
        with open("__data", "wb") as f:
            pickle.dump(_ecoute, f)

        MDDialog(
            title=translate("success", self.lang),
            text=translate("text_updated", self.lang),
            radius=[20, 7, 20, 7],
        ).open()

    def showpass(self, btn_num):
        try:
            state = self.root.ids[f'paste_{btn_num}'].password
            if btn_num:
                self.root.ids[f'paste_{btn_num}'].password = not state
                self.root.ids[f'eye_btn_{btn_num}'].icon = "eye-off" if state else "eye"
        except:
            pass

    def traduction(self, lang):
        self.lang = lang
        self.GUI.ids['label'].text = translate("entrer_texte", lang)
        self.GUI.ids['btn'].text = translate("enregistrer", lang)

        for i in range(1, 4):
            self.GUI.ids[f"paste_{i}"].hint_text = f"{translate('text', lang)} {i}"

        self.GUI.ids['toolbar'].right_action_items = [
            ["flag-outline", lambda x: self.traduction("en"), "EN", "EN"]
            if lang == "fr" else
            ["flag", lambda x: self.traduction("fr"), "FR", "FR"]
        ]

    def on_start(self):
        if os.path.isfile('__data'):
            with open("__data", "rb") as f:
                try:
                    data = pickle.load(f)
                    global _ecoute
                    for i in range(3):
                        _ecoute[i] = data[i]
                        self.GUI.ids[f'paste_{i+1}'].text = data[i]
                except:
                    pass


def getPid():
    if os.path.isfile('__pid'):
        with open('__pid', 'rb') as _pid:
            pid = pickle.load(_pid)
        try:
            os.kill(pid, signal.SIGINT)
        except Exception as err:
            print(err)


def setPid():
    with open('__pid', 'wb') as _pid:
        pickle.dump(os.getpid(), _pid)


if __name__ == '__main__':
    getPid()
    setPid()
    ecoute = Ecoute()
    ecoute.start()
    PersistentPASTE().run()

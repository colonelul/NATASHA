import time

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager

class KeyboardScreen(Screen):
    
    displayLabel = ObjectProperty()
    kbContainer = ObjectProperty()
    intr_temp = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(KeyboardScreen, self).__init__(**kwargs)
        self._add_keyboard()

    def _add_keyboard(self):
        layouts= "numeric_keyboard.json"
        self.kb = Window.request_keyboard(self._keyboard_close, self)
        
        if self.kb.widget:
            self._keyboard = self.kb.widget
            self._keyboard.layout = layouts
        else:
            self._keyboard = self.kb

        self._keyboard.bind(on_key_up=self.key_press)
    
    def _keyboard_close(self, *args):

        self._keyboard.unbind(on_key_up=self.key_press)
        self._keyboard = None

    def key_press(self, keyboard, keycode, *args):
        if keycode == "enter":
            self.kb.release()
            
            #self.manager.current = 'mode'
            
        print(keycode)
        self.displayLabel.text = keycode
        
        return True
    
    def change_lab(self, strr):
        if strr == '1':
            self.intr_temp.text = "Introduceti temperatura intre valorile 0-230*C"
        elif strr == '2':
            print("bau")
    
    def daa(self):
        self.manager.current = 'mode'

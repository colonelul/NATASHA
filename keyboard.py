from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from functools import partial
from SaveFile import ImportFile

class KeyboardScreen(Screen):
    
    displayLabel = ObjectProperty()
    kbContainer = ObjectProperty()
    intr_temp = ObjectProperty()
    temperature = ""
    
    def __init__(self, **kwargs):
        super(KeyboardScreen, self).__init__(**kwargs)
        self._add_keyboard()

    def _add_keyboard(self):
        layouts="numeric_keyboard.json"
        #partial(self.set_layout, layouts)
        
        self.kbContainer.add_widget(Button(
                    text="dai", size_hint= (.2, .2),
                    on_release=partial(self.set_layout, layouts)))
    
    def set_layout(self, layout, button):
        #Create Vkeyboard custom
        #a se vedea fisierul -> numeric_keyboard.json  
        self.kb = Window.request_keyboard(
            self._keyboard_release, self)
        if self.kb.widget:
            self._keyboard = self.kb.widget
            self._keyboard.layout = layout
        else:
            self._keyboard = self.kb

        self._keyboard.bind(on_key_up=self.key_press)
    
    def _keyboard_release(self, *args):
        self.focus = True
    
    def key_press(self, keyboard, keycode, *args):
        if keycode == "enter":
            #SerialConnection().send(self.temperature)
            self.clear_temp_label()
            self.kb.release()
            self.manager.current = "mode"
        elif keycode == "backspace":
            self.displayLabel.text = ""
        else:
            self.display_temp(keycode)
            
    def display_temp(self, keyy):
        if self.manager.screens[0].ids.share_data == 'heaters':
            self.temperature += u"{0}".format(keyy)
            if int(self.temperature) < 321 and self.temperature != "0" and self.temperature != "." and self.temperature != "":
                self.displayLabel.text = "Temperatura introdusa este: " + self.temperature + "*C"
            else:
                self.clear_temp_label()
                
        elif self.manager.screens[0].ids.share_data == 'bazin_cald':
            self.temperature += u"{0}".format(keyy)
            if int(self.temperature) < 90 and self.temperature != "0" and self.temperature != "." and self.temperature != "":
                self.displayLabel.text = "Temperatura introdusa este: " + self.temperature + "*C"
            else:
                self.clear_temp_label()
                
        elif self.manager.screens[0].ids.share_data == 'Hz':
            self.temperature += u"{0}".format(keyy)
            if int(self.temperature) < 60 and self.temperature != "0" and self.temperature != "." and self.temperature != "":
                self.displayLabel.text = "Temperatura introdusa este: " + self.temperature + "*C"
            else:
                self.clear_temp_label()
            
    def clear_temp_label(self):
        self.displayLabel.text = ""
        self.temperature = ""


from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager

Builder.load_string('''
<KeyboardScreen>:
    displayLabel: displayLabel
    kbContainer: kbContainer
    intr_temp: intr_temp
    
    BoxLayout:
        orientation: 'vertical'
        Label:
            id: intr_temp
            size_hint_y: 0.15
            text: "Introduceti o temperatura"
        Button:
            text: "Back"
            size_hint_y: 0.1
            on_release: root.daa()
        BoxLayout:
            id: kbContainer
            size_hint_y: 0.2
            orientation: "horizontal"
            padding: 10
        Label:
            id: displayLabel
            size_hint_y: 0.15
            markup: True
            text: "[b]Key pressed[/b] - None"
            halign: "center"
        Widget:
            # Just a space taker to allow for the popup keyboard
            size_hint_y: 0.5

''')

class KeyboardScreen(Screen):
    
    displayLabel = ObjectProperty()
    kbContainer = ObjectProperty()
    intr_temp = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(KeyboardScreen, self).__init__(**kwargs)
        self._keyboard = None
        #self._add_keyboard()

    def _add_keyboard(self):
        layouts= "numeric_keyboard.json"
        kb = Window.request_keyboard(self._keyboard_close, self)
        
        if kb.widget:
            self._keyboard = kb.widget
            self._keyboard.layout = layouts
        else:
            self._keyboard = kb

        self._keyboard.bind(on_key_up=self.key_press)
    
    def _keyboard_close(self, *args):

        self._keyboard.unbind(on_key_up=self.key_press)
        self._keyboard = None

    def key_press(self, keybard, keycode, *args):
        if keycode == "enter":
            print("HAM")
            self.daa()
            
        print(keycode)
        self.displayLabel.text = keycode
    
    def change_lab(self, strr):
        if strr == '1':
            self.intr_temp.text = "Introduceti temperatura intre valorile 0-230*C"
        elif strr == '2':
            print("bau")
    def daa(self):
        self.manager.current = 'mode'

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from functools import partial
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager

Builder.load_string('''
<KeyboardScreen>:
    displayLabel: displayLabel
    kbContainer: kbContainer
    BoxLayout:
        orientation: 'vertical'
        Label:
            size_hint_y: 0.15
            text: "Introduceti o temperatura"
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
        Button:
            text: "Back"
            size_hint_y: 0.1
            on_release: root.manager.current = "mode"
        Widget:
            # Just a space taker to allow for the popup keyboard
            size_hint_y: 0.5

''')

class KeyboardScreen(Screen):

    displayLabel = ObjectProperty()
    kbContainer = ObjectProperty()

    def __init__(self, **kwargs):
        super(KeyboardScreen, self).__init__(**kwargs)
        self._keyboard = None

    def _add_keyboard(self):
        layouts= "numeric_keyboard.json"
        kb = Window.request_keyboard(self._keyboard_close, self)
        if kb.widget:

            self._keyboard = kb.widget
            self._keyboard.layout = layouts
        else:
            self._keyboard = kb

        self._keyboard.bind(on_key_down=self.key_down,
                            on_key_up=self.key_up)

    def _keyboard_close(self, *args):

        if self._keyboard:
            self._keyboard.unbind(on_key_down=self.key_down)
            self._keyboard.unbind(on_key_up=self.key_up)
            self._keyboard = None

    def key_down(self, keyboard, keycode, text, modifiers):

        self.displayLabel.text = u"Key pressed - {0}".format(text)

    def key_up(self, keyboard, keycode, *args):

        if isinstance(keycode, tuple):
            keycode = keycode[1]
        self.displayLabel.text += u" (up {0})".format(keycode)



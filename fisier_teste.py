from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from functools import partial
from kivy.config import Config
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy import require

# This example uses features introduced in Kivy 1.8.0, namely being able
# to load custom json files from the app folder.
require("1.8.0")

Builder.load_string('''
<KeyboardScreen>:
    displayLabel: displayLabel
    kbContainer: kbContainer
    BoxLayout:
        orientation: 'vertical'
        Label:
            size_hint_y: 0.15
            text: "Available Keyboard Layouts"
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
    """
    Screen containing all the available keyboard layouts. Clicking the buttons
    switches to these layouts.
    """
    displayLabel = ObjectProperty()
    kbContainer = ObjectProperty()

    def __init__(self, **kwargs):
        super(KeyboardScreen, self).__init__(**kwargs)
        self._add_keyboards()
        self._keyboard = None

    def _add_keyboards(self):
        """ Add a buttons for each available keyboard layout. When clicked,
        the buttons will change the keyboard layout to the one selected. """
        # Add the file in our app directory, the .json extension is required.
        layouts= "numeric_keyboard.json"
        self.kbContainer.add_widget(Button(text="key", on_release=partial(self.set_layout, layouts)))

    def set_layout(self, layout, button):
        """ Change the keyboard layout to the one specified by *layout*. """
        kb = Window.request_keyboard(
            self._keyboard_close, self)
        if kb.widget:
            # If the current configuration supports Virtual Keyboards, this
            # widget will be a kivy.uix.vkeyboard.VKeyboard instance.
            self._keyboard = kb.widget
            self._keyboard.layout = layout
        else:
            self._keyboard = kb

        self._keyboard.bind(on_key_down=self.key_down,
                            on_key_up=self.key_up)

    def _keyboard_close(self, *args):
        """ The active keyboard is being closed. """
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self.key_down)
            self._keyboard.unbind(on_key_up=self.key_up)
            self._keyboard = None

    def key_down(self, keyboard, keycode, text, modifiers):
        """ The callback function that catches keyboard events. """
        self.displayLabel.text = u"Key pressed - {0}".format(text)

    # def key_up(self, keyboard, keycode):
    def key_up(self, keyboard, keycode, *args):
        """ The callback function that catches keyboard events. """
        # system keyboard keycode: (122, 'z')
        # dock keyboard keycode: 'z'
        if isinstance(keycode, tuple):
            keycode = keycode[1]
        self.displayLabel.text += u" (up {0})".format(keycode)


class KeyboardDemo(App):
    sm = None  # The root screen manager

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(KeyboardScreen(name="keyboard"))
        self.sm.current = "keyboard"
        return self.sm


if __name__ == "__main__":
    KeyboardDemo().run()
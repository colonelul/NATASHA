from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from functools import partial

class KeyboardScreen():

    displayLabel = ObjectProperty()
    kbContainer = ObjectProperty()

    def __init__(self, **kwargs):
        super(KeyboardScreen, self).__init__(**kwargs)
        self._add_keyboards()
        self._keyboard = None

    def _add_keyboards(self):
        layouts= "numeric_keyboard.json"
        self.kbContainer.add_widget(Button(text="key", on_release=partial(self.set_layout, layouts)))

    def set_layout(self, layout, button):
        kb = Window.request_keyboard(
            self._keyboard_close, self)
        if kb.widget:

            self._keyboard = kb.widget
            self._keyboard.layout = layout
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

    # def key_up(self, keyboard, keycode):
    def key_up(self, keyboard, keycode, *args):

        # system keyboard keycode: (122, 'z')
        # dock keyboard keycode: 'z'
        if isinstance(keycode, tuple):
            keycode = keycode[1]
        self.displayLabel.text += u" (up {0})".format(keycode)


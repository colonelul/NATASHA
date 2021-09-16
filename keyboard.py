from kivy.core.window import Window

class Keyboard:
    def open(self):
        keyboard = Window.request_keyboard(
        self._keyboard_close, self)
        if keyboard.widget:
            vkeyboard = self._keyboard.widget
            vkeyboard.layout = 'numeric.json'
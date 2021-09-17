# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 11:18:48 2021

@author: NeluColoNelu
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from DataFile import CacheFile
from kivy.config import Config
from kivy.clock import Clock
from time import strftime
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

Config.set('graphics', 'width', '1080')
Config.set('graphics', 'height', '720')

kv_file = Builder.load_file("mainui.kv")

class MainWindow(Screen):
    tempContainer = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self._temperatures_widget()
    
    def update_time(self, cok):
        self.root.ids.time.text = strftime('[b]%H[/b]:%M:%S')
        
    def on_start(self):
        print("da")
        Clock.schedule_interval(self.update_time, 0)
    
    def _temperatures_widget(self):
        name_temp = ["Duza", "T1", "T2", "T3", "T4", "T5", "T6", "t7", "T8", "T9"]
        for key in name_temp:
            self.tempContainer.add_widget(
                Label(text=key), 0)
        for key in name_temp:
            self.tempContainer.add_widget(
                Label(text='0'), 1)
        for key in name_temp:
            self.tempContainer.add_widget(
                TextInput())
        
class Settings(Screen):
    print("settings")

class Plots(Screen):
    print("plots")

class MainUiApp(App):
    sm = None
    
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainWindow(name="mode"))
        self.sm.add_widget(Settings(name="settings"))
        self.sm.add_widget(Plots(name="plots"))
        
        self.sm.current = "mode"
        return self.sm

if __name__== '__main__':
    MainUiApp().run()



# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 11:18:48 2021

@author: NeluColoNelu
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from DataFile import CacheFile
from kivy.config import Config
from kivy.clock import Clock
from time import strftime

Config.set('graphics', 'width', '1080')
Config.set('graphics', 'height', '720')

class MainWindow(Screen):
    
    def update_time(self, cok):
        self.root.ids.time.text = strftime('[b]%H[/b]:%M:%S')
        
    def on_start(self):
        print("da")
        Clock.schedule_interval(self.update_time, 0)

class Settings(Screen):
    print("settings")

class Plots(Screen):
    print("plots")
    
class WindowManager(ScreenManager):
    pass

kv_file = Builder.load_file("mainui.kv")

win = WindowManager()

screens = [MainWindow(name="main"), Settings(name="settings"), Plots(name="plots")]    
for screen in screens:
    win.add_widget(screen)

win.current = "main"

class MainUiApp(App):
    def build(self):
        return win

if __name__== '__main__':
    MainUiApp().run()



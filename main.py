# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 11:18:48 2021

@author: NeluColoNelu
"""
import threading
import time

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.clock import Clock, mainthread
from time import strftime
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors.focus import FocusBehavior

from serial import SerialConnection
from SaveFile import ImportFile
from keyboard import KeyboardScreen

Config.set('graphics', 'width', '1080')
Config.set('graphics', 'height', '720')

kv_file = Builder.load_file("mainui.kv")

class MainWindow(Screen):
    name_temp = ["Duza", "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9"]
    tempContainer = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.arr_temp = None
        self.arr_rpm = None
        self._temperatures_widget()
        self.start_first_thread()
    
    def start_first_thread(self):
        threading.Thread(target=self.first_thread).start()
    
    def first_thread(self):
            # val = self.separate_data_serial() 
            # self.update_label(val)
        print("Thread")
               
    
    @mainthread
    def update_label(self, txt):
        self.change_text_label(txt)
        
    def update_time(self):
        self.root.ids.time.text = strftime('[b]%H[/b]:%M:%S')
        
    def on_start(self):
        Clock.schedule_interval(self.update_time(), 0)
        
    def on_focus(self, instance, value):
        self.manager.current = 'keyboard'
        if instance in self.ids.values():
            print(list(self.ids.keys())[list(self.ids.values()).index(instance)])  

    def _temperatures_widget(self):
        
        for key in self.name_temp:
            lab = Label(text=key)
            self.tempContainer.add_widget(lab, 0)
            
        for key in self.name_temp:
            lab = Label(text='0')
            self.ids[key + "-lab"] = lab
            self.tempContainer.add_widget(lab, 1)
            
        for key in self.name_temp:
            text = TextInput()
            self.ids[key + "-text"] = text
            self.tempContainer.add_widget(text)
            text.bind(focus=self.on_focus)

            
        self.change_text_label(None)
        
    def separate_data_serial(self):
        dat_receiv = SerialConnection()
        data_received = SerialConnection.get_data(dat_receiv)
        
        if len(data_received) > 0:
            try:
                if data_received[0] == 't':
                    self.arr_temp[int(data_received[
                        data_received.find('t') + 1:data_received.find('=')])] = data_received[
                            data_received.find('=') + 1:data_received.find('.') + 2]
                elif data_received[0] == 'r':
                    self.arr_rpm[int(data_received[
                        data_received.find('r') + 1:data_received.find('=')])] = data_received[
                            data_received.find('=') + 1:data_received.find('.') + 2]
                elif data_received[0] == 'd':
                    self.arr_temp[12] = data_received[data_received.find('=') + 1:data_received.find('.') + 2]
            except:
                pass
            
        return self.arr_temp
            
    def change_text_label(self, values):
        
        if values == None:
            data_file_object = ImportFile()
            import_file = ImportFile.load(data_file_object)
            
        for key in self.name_temp:
            if key == "Duza": 
                self.ids[key + "-lab"].text = str(import_file['duza'])
            else:
                self.ids[key + "-lab"].text = str(import_file[key])
        
class Settings(Screen):
    print("settings")

class Plots(Screen):
    print("plots")

class MainUiApp(App):
    sm = None
    
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainWindow(name='mode'))
        self.sm.add_widget(Settings(name='settings'))
        self.sm.add_widget(Plots(name='plots'))
        self.sm.add_widget(KeyboardScreen(name='keyboard'))
        
        self.sm.current = 'mode'
        return self.sm

if __name__== '__main__':
    MainUiApp().run()



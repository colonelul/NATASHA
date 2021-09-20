# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 11:18:48 2021

@author: NeluColoNelu
"""
import threading

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.clock import Clock, mainthread
from time import strftime
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from serial import SerialConnection
from SaveFile import ImportFile

Config.set('graphics', 'width', '1080')
Config.set('graphics', 'height', '720')

kv_file = Builder.load_file("mainui.kv")

class DragableObject:
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            return True

class MainWindow(Screen):
    name_temp = ["Duza", "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9"]
    tempContainer = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.arr_temp = None
        self.arr_rpm = None
        self.serial_start()
        data_file_object = ImportFile()
        self.import_file = ImportFile.load(data_file_object)
        self._temperatures_widget()
        #self.on_start()
    
    def serial_start(self):
        serial = SerialConnection()
    
    def start_frist_thread(self):
        threading.Thread(target=self.first_thread).start()
    
    def start_second_thread(self):
        threading.Thread(target=self.second_thread).start()
    
    def first_thread(self):
        val = self.separate_data() 
        
        self.update_label_text(val)
        
        
    def second_thread(self):
        self.update_label_text()
        
        
    
    @mainthread
    def update_label_text(self, new_text):
        self.change_text()
        
    
    def update_time(self, cok):
        self.root.ids.time.text = strftime('[b]%H[/b]:%M:%S')
        
    def on_start(self):
        Clock.schedule_interval(self.update_time, 0)
    
    def _temperatures_widget(self):
        
        for key in self.name_temp:
            lab = Label(text=key + str('\u2103'))
            self.tempContainer.add_widget(lab, 0)
            
        for key in self.name_temp:
            lab = Label(text='0')
            self.ids[key + "-lab"] = lab
            self.tempContainer.add_widget(lab, 1)
            
        for key in self.name_temp:
            text = TextInput()
            self.ids[key + "-text"] = text
            self.tempContainer.add_widget(text)
            
        self.change_text(self.name_temp)
        
    def separate_date(self):
        data_received = SerialConnection.get_data()
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
            
    def change_text(self, text_input):
        for key in self.name_temp:
            if key == "Duza": 
                self.ids.key.text = text_input[int('d')]
            else:
                self.ids.key.text = text_input[int(key)]
    
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



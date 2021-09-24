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
from openSerial import SerialConnection
from SaveFile import ImportFile
from keyboard import KeyboardScreen

Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '1024')
Config.set('kivy', 'keyboard_mode', 'dock')
Config.write()


kv_file = Builder.load_file("main-design.kv")

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
        SerialConnection().__connect__()
        Clock.schedule_interval(self.update_time(), 0)
               
    @mainthread
    def update_label(self, txt):
        self.change_text_label(txt)
        
    def update_time(self):
        self.ids.time.text = '[b][color=#9e3898]'+'[size=80]'+strftime('%I:%M:%S')+'[/size]'+'[/color][/b]'

        
    ''' Traducerea valorilor din change_bob
            Fiecare valoare are o temp MAXIMA
            1 -> Duza, T1,...,T9 (0-230*C)
            2 -> T11             (0-90*C)            
    '''
    
    def on_focus(self, instance, value):
        self.manager.current = 'keyboard'
        if instance in self.ids.values():
            txt_focuses = list(self.ids.keys())[list(self.ids.values()).index(instance)]
            for txt in self.name_temp:
                if txt + "-text" == txt_focuses:
                    self.manager.screens[3].ids.intr_temp.text = "Introduceti o temperatura cumprinsa intre valorile 0 - 320*C"
                    self.manager.screens[0].ids.share_data = "heaters"
            print(txt_focuses, value)
        
    def _temperatures_widget(self):
        
        for key in self.name_temp:
            lab = Label(text=key)
            self.tempContainer.add_widget(lab, 0)
            
        for key in self.name_temp:
            lab = Label(text='0')
            self.ids[key + "-lab"] = lab
            self.tempContainer.add_widget(lab, 1)
            
        for key in self.name_temp:
            text = TextInput(input_filter='float')
            self.ids[key + "-text"] = text
            self.tempContainer.add_widget(text)
            text.bind(focus=self.on_focus)
        
        self.ids.amp.bind(focus=self.on_focus)
        self.ids.calda_input.bind(focus=self.on_focus)
    
        self.change_text_label(None)
        
    def separate_data_serial(self):
        data_received = SerialConnection().get_data()
        
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
    def dada(self):
        self.manager.current = 'mode'

class Plots(Screen):
    pass

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



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
from kivy.properties import ObjectProperty, StringProperty
from kivy.config import Config
from kivy.clock import Clock, mainthread
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from openSerial import SerialConnection, Connection
from SaveFile import ImportFile
from keyboard import KeyboardScreen

Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '1024')
Config.set('kivy', 'keyboard_mode', 'dock')
Config.write()


kv_file = Builder.load_file("main-design.kv")

class MainWindow(Screen):
    name_temp = ["Duza", "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9"]
    buttons = {'motor': False, 'heaters': False, 'pompa': False}
    tempContainer = ObjectProperty()
    clock_time = StringProperty("")
    
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.value_laserToSend = bytearray(b'\x01\x03\x00a\x00\x01\xd5\xd4')
        self.arr_temp = None
        self.arr_rpm = None
        self._create_widgets()
        self.start_first_thread()
    
    
    
    def start_first_thread(self):
        t1 = threading.Thread(target=self.first_thread)
        t1.daemon = True
        t1.start()
    
    def first_thread(self):
        SerialConnection().__connect__()
               
    @mainthread
    def update_label(self, txt):
        self.change_text_onStart(txt)
    
    def on_focus(self, instance, value):
        self.manager.current = 'keyboard'
        if instance in self.ids.values():
            txt_focuses = self.key_to_id(instance)
            if txt_focuses[0 : txt_focuses.find("_")] + "_text" == txt_focuses:
                self.manager.screens[3].ids.intr_temp.text = "Introduceti o temperatura cuprinsa intre valorile 0 - 320*C"
                self.manager.screens[0].ids.share_data = "heaters"
            elif txt_focuses == "bazinCald_text":
                self.manager.screens[3].ids.intr_temp.text = "Introduceti o temperatura cuprinsa intre valorile 0 - 90*C"
                self.manager.screens[0].ids.share_data = "bazin_cald"
            elif txt_focuses == "hz_text":
                self.manager.screens[3].ids.intr_temp.text = "Introduceti o hrecventa cuprinsa intre valorile 0 - 60Hz"
                self.manager.screens[0].ids.share_data = "Hz"
            
            try:
                self.ids[txt_focuses[0 : txt_focuses.find("_")] + "_lab"].text = self.ids[txt_focuses].text
            except:
                pass
            
            if len(self.ids[txt_focuses].text) > 0 and value:
                self.ids[txt_focuses].text = ""
                            
            ImportFile().export_file(txt_focuses[0 : txt_focuses.find("_")], self.ids[txt_focuses[0 : txt_focuses.find("_")] + "_lab"].text)
                
    def _create_widgets(self):
        
        for key in self.name_temp:
            lab = Label(text="[b][color=#000000]" + key + "[/color][/b]", markup=True, font_size="20sp")
            self.tempContainer.add_widget(lab)
            
        for keyy in self.name_temp:
            lab = Label(text='0')
            self.ids[keyy + "_lab"] = lab
            self.tempContainer.add_widget(lab)
             
        for keyyy in self.name_temp:
            text = TextInput(input_filter='float', size_hint= (.8, None), height= 30)
            self.ids[keyyy + "_text"] = text
            self.tempContainer.add_widget(text)
            text.bind(focus=self.on_focus)
        
        for keyyy in range(10):
            lab = Label(text="[b][color=#000000]FAN:[/color]\n0%[/b]", markup=True, font_size="16sp")
            self.ids["rpm" + str(keyyy)] = lab
            self.tempContainer.add_widget(lab)
        
        self.ids.hz_text.bind(focus=self.on_focus)
        self.ids.bazinCald_text.bind(focus=self.on_focus)
        self.ids.heaters.bind(state=self.buttons_listen)
        self.ids.motor.bind(state=self.buttons_listen)
        self.ids.motor_plus.bind(state=self.buttons_listen)
        self.ids.motor_minus.bind(state=self.buttons_listen)
        
        self.change_text_onStart(None)
        
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
            
    def change_text_onStart(self, values):
        
        if values == None:
            import_file = ImportFile().add(None)

        for key in self.name_temp:
            if key == "Duza": 
                self.ids[key + "_lab"].text = str(import_file['duza'])
            else:
                self.ids[key + "_lab"].text = str(import_file[key])
    
    def update_time(self):
        #self.clock_time = time.strftime("%H:%M:%S")
        Connection.send(self.value_laserToSend)
        data = Connection.get_data()
        
        print(data)
        
    def buttons_listen(self, instance, value):
        if value == "down":
            idd = self.key_to_id(instance)
            if idd in self.buttons:
                self.send_to_serial(idd+"-start" if self.buttons[idd] else idd+"-stop")
                if self.buttons[idd]:
                    self.ids[idd].background_color = (0, 210/255, 0)
                    if idd == "heaters":   
                        self.ids[idd].text = "START Incalzire"
                    elif idd == "motor":
                        self.ids[idd].text = "START Motor"
                else:
                    self.ids[idd].background_color = (250/255, 0, 0)
                    if idd == "heaters":   
                        self.ids[idd].text = "STOP Incalzire"
                    elif idd == "motor":
                        self.ids[idd].text = "STOP Motor"
                
                self.buttons[idd] = not self.buttons[idd]
                        
            elif idd == "motor_plus":
                self.send_to_serial("motor_plus")
            elif idd == "motor_minus":
                self.send_to_serial("motor_minus")

        
    def key_to_id(self, inst):
        return list(self.ids.keys())[list(self.ids.values()).index(inst)]
    
    def send_to_serial(self, send):
        sendd = SerialConnection()
        papa = SerialConnection.send(sendd, send)
    
class Settings(Screen):
    def dada(self):
        self.manager.current = 'mode'

class Plots(Screen):
    pass

class SScreenManager(ScreenManager):
    pass

class PopUp:
    def err_worning():
        pass
    
    def err_dead():
        pass

class MainUiApp(App):
    sm = None
    
    def build(self):
        bau = MainWindow()
        Clock.schedule_interval(lambda dt: bau.update_time(), 1)
        
        self.sm = ScreenManager()
        self.sm.add_widget(MainWindow(name='mode'))
        self.sm.add_widget(Settings(name='settings'))
        self.sm.add_widget(Plots(name='plots'))
        self.sm.add_widget(KeyboardScreen(name='keyboard'))
        
        self.sm.current = 'mode'
        return self.sm

if __name__== '__main__':
    MainUiApp().run()



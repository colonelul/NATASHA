# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 11:18:48 2021
@author: NeluColoNelu"""

import threading
import time
import openSerial
import cv2

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.config import Config
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics.texture import Texture
from SaveFile import ImportFile
from keyboard import KeyboardScreen
from filamentDimension import MeasuringObject

Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '1024')
Config.set('kivy', 'keyboard_mode', 'dock')
Config.write()

kv_file = Builder.load_file("main-design.kv")

class MainWindow(Screen):
    
    name_temp = ["Duza", "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9"]
    buttons = {'motor': False, 'heaters': False, 'pompa': False}
    devices_adress = {'laser': '01', 'hault': '02', 'motor_extrusie': '03'}
    tempContainer = ObjectProperty()
    clock_time = StringProperty("")
    temperatures = NumericProperty
    fps = NumericProperty(30)
    Start = 1
    
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.value_laserToSend = bytearray(b'\x01\x03\x00a\x00\x01\xd5\xd4')
        self.arr_temp = None
        self.arr_rpm = None
        self.data_receive = None
        self.motorFilament_status = False
        self.capture = cv2.VideoCapture(0)
        openSerial.connect()
        self._create_widgets()   
        self.start_first_thread()
    
    def start_first_thread(self):
        threading.Thread(target=self.first_thread, daemon = True).start()
        self.start_second_thread()
    def start_second_thread(self):
        threading.Thread(target=self.second_thread, daemon = True).start()
        self.start_three_thread()
    def start_three_thread(self):
        threading.Thread(target=self.three_thread, daemon = True).start()
    
    def first_thread(self):
        self.motorFilament()
        Clock.schedule_interval(lambda dt: self.send_dat(), 0.10)
    def second_thread(self):
        Clock.schedule_interval(lambda dt: self.update_camera(), 1.0 / self.fps)
    def three_thread(self):
        Clock.schedule_interval(lambda dt: self.update_GUI(), 1 / 10)
    
    def send_dat(self):
        
        if not(self.motorFilament_status):
            self.motorFilament()
        
        time.sleep(5.0 / 100)
        
        openSerial.send(self.value_laserToSend)
        
        self.data_receive = self.get_dat()

    def motorFilament(self):
        rs = RS485()
        if rs.RS485_onStart('start'): 
            self.motorFilament_status = True 
        else: 
            self.motorFilament_status = False
    
    def get_dat(self):
        data = openSerial.get_data()
        return data
        
    def update_camera(self):
        try:
            ret, frame = self.capture.read()
            buf = cv2.flip(frame, 0).tostring()
            try:
                cc = MeasuringObject().process_image(frame)
                self.ids.filament_camera.text = cc
            except:
                pass
            
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]))
            texture.blit_buffer(buf, bufferfmt="ubyte")
            self.ids.camera.texture = texture
        except:
            pass
    
    def update_GUI(self):
        self.ids.clock.text = time.strftime("%H:%M:%S")
        if self.data_receive != None:
            if self.data_receive[:2] == self.devices_adress['laser']:
                try:
                    data_str = str(float.fromhex(self.data_receive[6:10])*0.001)
                    self.ids.dFilament_laser.text = "[b]Dimensiune filament(Laser): [/b]" + data_str
                except:
                    pass
                
            if self.data_receive[:2] == self.devices_adress['hault']:
                self.motorFilament_status = True
                print("motor - > " + str(self.data_receive))
    
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
            
            #ImportFile().export_file(txt_focuses[0 : txt_focuses.find("_")], self.ids[txt_focuses[0 : txt_focuses.find("_")] + "_lab"].text)
                
    def _create_widgets(self):
        
        for key in self.name_temp:
            lab = Label(text="[b][color=#000000]" + key + "[/color][/b]", markup=True, font_size="20sp")
            self.tempContainer.add_widget(lab)
            
        for keyy in self.name_temp:
            lab = Label(text=str(self.temperatures))
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
        self.ids.hz_text.bind(focus=self.on_focus)
        
        self.change_text_onStart(None)
        
    def separate_data_serial(self):
        data_received = openSerial.get_data()
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
        
    def buttons_listen(self, instance, value):
        if value == "down":
            idd = self.key_to_id(instance)
            if idd in self.buttons:
                openSerial.send(idd+"-start" if self.buttons[idd] else idd+"-stop")
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
    
    def motor_run(self):
        if self.motorFilament_status == 'Start':
            RS485().motor_run()
    
class Settings(Screen):
    old_value = None
    new_value = None
    stop = True
    def __init__(self, **kwargs):
        super(Settings, self).__init__(**kwargs)
        self.ids.hault_text.bind(focus=self.on_focus)
    
    def on_focus(self, instance, value):
        if self.key_to_id(instance) == 'hault_text':
            text = self.ids.hault_text.text
            if len(text) > 0 and value:
                self.ids.hault_text.text = ""
    
    def key_to_id(self, inst):
        return list(self.ids.keys())[list(self.ids.values()).index(inst)]

    def hault_motor(self):
        if len(self.ids.hault_text.text) > 0:
            self.old_value = int(self.ids.hault_text.text) if self.old_value == None else self.new_value
            self.new_value = int(self.ids.hault_text.text)
            ss = RS485()
            self.stop = ss.motor_run(self.stop, self.old_value, self.new_value)
    def hault_stop(self):
        s = RS485()
        self.stop = s.motorStop()
        
class Plots(Screen):
    pass

class SScreenManager(ScreenManager):
    pass

class PopUp:
    def err_worning():
        pass
    
    def err_dead():
        pass

class RS485:
    def __init__(self):
        self.send_array = {'start':      [0x02, 0x06, 0x02, 0x3C, 0x0, 0x05, 0x00, 0x00],
                           'after-start':[0x02, 0x06, 0x03, 0x0C, 0x0, 0x81, 0x00, 0x00],
                           'stop':       [0x2,  0x6,  0x04, 0x0E, 0x0, 0x00, 0x00, 0x00],
                           'run':        [0x2,  0x6,  0x04, 0x0A, 0x0, 0x00, 0x00, 0x00],
                           'after-run':  [0x2,  0x6,  0x04, 0x0E, 0x0, 0x81, 0x00, 0x00]}
        
    def CRC(self, cnt, status):
        CRC_result = 0xFFFF
        for c in range(cnt + 1):
            CRC_result ^= self.send_array[status][c]
            for cc in range(8):
                if CRC_result & 0x01:
                    CRC_result = CRC_result >> 1
                    CRC_result ^= 0xA001
                else:
                    CRC_result = CRC_result >> 1
        
        hhh,lll = CRC_result.to_bytes(2, 'big')
        
        self.send_array[status][6] = lll
        self.send_array[status][7] = hhh
        
        if openSerial.send(bytearray(self.send_array[status])):
            #print(self.send_array[status])
            return True
            
    def RS485_onStart(self, index):
        if self.CRC(5, index):
            read_data = openSerial.get_data()
            if read_data != None and read_data[:2] == '02':
                time.sleep(5.0 / 100)
                if self.CRC(5, 'after-start'):
                    return True
    
    def motorStop(self):
        self.CRC(5, 'stop')
        return True
    
    def motor_run(self, stop, old_text, new_text):
        if old_text != new_text:
            return self.delay_speed(stop, old_text, new_text)
        else:
            return self.run(stop, new_text)
        
    def run(self, stop, go):
        h,l = go.to_bytes(2, 'big')
        self.send_array['run'][4] = h
        self.send_array['run'][5] = l
        if stop:
            self.CRC(5, 'run')
            time.sleep(3.0 / 100)
            self.CRC(5, 'after-run')
            time.sleep(3.0 / 100)
            return False
        else:
            time.sleep(5.0 / 100)
            self.CRC(5, 'run')
            return False
    
    def delay_speed(self, stop, old, new):
        while new > old:
            if new - old > 50:
                old += 50
            else:
                old += new - old
            time.sleep(10 / 100)
            cox = self.run(stop, old)
        while new < old:
            if old - new > 50:
                old -= 50
            else:
                old -= old - new
            time.sleep(10 / 100)
            cox = self.run(stop, old)
        return cox
        
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



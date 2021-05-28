import kivy
import socket
import selectors
import numpy as np
import threading
import time
import pyowm
from datetime import timedelta, datetime, date
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation    
from kivy.clock import Clock
import calendar

Window.clearcolor = (37/255.0, 53/255.0, 74/255.0,1)

Window.size = (888, 400)

PORT = 2040
HOST = '192.168.1.40'  
address_Write = ''
flag_error_connect = "0"
flag_sts_connect = "0"

def Connecting(dic=True):
    while True:
        global flag_error_connect,flag_sts_connect, HOST, PORT
        print(HOST)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(0.1)
        try:
            client.connect((HOST,PORT))
            flag_error_connect = "1"
            flag_sts_connect = "1"
        except:
            flag_error_connect = "0"
            flag_sts_connect = "0"
            print("error")
        
        time.sleep(0.5)

def Write_register(HOST, address, data, port=PORT, dic=True):
    '''
        Finally used the ASCII code
    '''
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    str1= "500000FF03FF00001C000014010000D*"+address+"0001"+data
    msg1 = str1.encode()
    client.send(msg1)

def dectohex(number):
    data = hex(number)
    data = data.replace('0','',1)
    data = data.replace('x','',1)
    if len(data) == 1:
        return '000' + data
    elif len(data) == 2:
        return '00' + data
    elif len(data) == 3:
        return '0' + data
    else:
        return data

def format_len_data_write(data):
    _data = data
    while len(_data)<6:
        _data = '0' + _data
    return _data

class MainWindow(Screen):
    global address_Write, HOST, PORT
    def get_content_write(self):        
        self.address_write = self.ids.id_content_address_meomory_write.text
        self.address_write = format_len_data_write(self.address_write)        
        self.content_write = self.ids.id_content_write.text
        self.content_write = dectohex(int(self.content_write))  
        Write_register(HOST,self.address_write,self.content_write)
    
    def btnConnect(self, widget, *args):         
        global flag_error_connect,flag_sts_connect, HOST, PORT
        HOST = self.ids.kv_IP_PLC.text
        if flag_error_connect == "0" and flag_sts_connect == "0":
            anim = Animation(kv_ColorBackgroud_btnConnect = (1,0,0,1))
            self.ids.kv_txtStatus_btnConnect.text = "DISCONNECTED"
            anim.start(widget)
        if flag_error_connect == "1" and flag_sts_connect == "1":
            anim = Animation(kv_ColorBackgroud_btnConnect = (0,1,0,1))
            self.ids.kv_txtStatus_btnConnect.text = "CONNECTED"
            anim.start(widget)

class LightWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('Main.kv')

class MainApp(App):
    def build(self):
        return kv

              

if __name__ == "__main__":
    threading.Thread(target=Connecting).start()
    MainApp().run()




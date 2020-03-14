'''
实验名称：W5500以太网模块MQTT通信
版本：v1.0
日期：2019.11
作者：01Studio
说明：通过Socket编程实现pyBoard+W5500以太网模MQTT通信  订阅者（subscribe）。
'''

import network,pyb,time
from machine import I2C,Pin
from ssd1306 import SSD1306_I2C
from simple import MQTTClient

#初始化OLED
i2c = I2C(sda=Pin('Y10'), scl=Pin('Y9'))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

#初始化以太网模块
nic = network.WIZNET5K(pyb.SPI(2), pyb.Pin.board.Y5, pyb.Pin.board.Y4)
nic.active(True)
nic.ifconfig('dhcp')

#设置MQTT回调函数,有信息时候执行
def MQTT_callback(topic, msg):
    print('topic: {}'.format(topic))
    print('msg: {}'.format(msg))


#判断网络是否连接成功
if nic.isconnected():

    print(nic.ifconfig()) #打印IP信息

    #OLED数据显示
    oled.fill(0)   #清屏背景黑色
    oled.text('IP/Subnet/GW:',0,0)
    oled.text(nic.ifconfig()[0], 0, 20)
    oled.text(nic.ifconfig()[1],0,38)
    oled.text(nic.ifconfig()[2],0,56)
    oled.show()

    SERVER = 'mqtt.p2hp.com'
    PORT = 1883
    CLIENT_ID = '01Studio-pyBoard' # 客户端ID
    TOPIC = '/public/01Studio/1' # TOPIC名称

    client = MQTTClient(CLIENT_ID, SERVER, PORT)
    client.set_callback(MQTT_callback)  #配置回调函数
    client.connect()
    client.subscribe(TOPIC) #订阅主题

    while (True):
        client.check_msg() #检测是否收到信息，收到则执行回调函数打印。
        time.sleep_ms(300) #接收间隔

#!/usr/bin/env python3
# coding: UTF-8

from pyGPIO.gpio import gpio, connector, port
import subprocess
from time import sleep
from datetime import datetime
from sys import exit
import os
from os.path import join, dirname
from random import randrange
from dotenv import load_dotenv

if not os.getegid() == 0:
    exit('Script must be run as root')


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SAVE_DIR = os.environ["SAVE_DIR"]

# ボタンを繋いだGPIO
BUTTON_PIN = port.GPIO12
tshark = None

def getNowDateTimeString():
    return datetime.today().strftime("%Y%m%d%H%M%S")

def stopPacketCapture():
    if tshark is not None:
        tshark.terminate()

def startPacketCapture(fileName):
    stopPacketCapture()
    print("Starting...")
    sleep(3)
    global tshark
    tshark = subprocess.Popen(["tshark", "-w", fileName])

def shutdown():
    subprocess.run(['/sbin/shutdown', '-h', '-t', '5'])

def main():
    # GPIO初期化
    print("Initializing GPIO...")
    gpio.init()
    gpio.setcfg(BUTTON_PIN, gpio.INPUT)
    # 端子に何も接続されていない場合の状態を設定
    # 3.3Vの場合には「2」（プルアップ）
    # 0Vの場合は「1」と設定する（プルダウン）
    gpio.pullup(BUTTON_PIN, gpio.PULLUP)

    print("Waiting for Ethernet...")
    sleep(30)
    rand = randrange(100000, 999999)
    fileName = join(SAVE_DIR, getNowDateTimeString() + "_" + str(rand) + ".pcap")
    startPacketCapture(fileName)

    loop = None
    while True:
        isPushed = gpio.input(BUTTON_PIN) == 0
        #  ボタンに変化があったとき
        if isPushed != loop:
            #  ボタンが押された時
            if isPushed == True:
                print("pushed!")
                stopPacketCapture()
                shutdown()
                break

            loop = isPushed

        sleep(0.5)

main()

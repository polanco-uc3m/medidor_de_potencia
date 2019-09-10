#-*-coding:utf-8-*-
# ALSTOM SIGNAILLING SPAIN
# MV 49: CUSTOMER CARE
# Author Antonio Polanco Belmonte
# April 2019
#-------------------------------------------------------------------------------
import time
import os
import shutil
import subprocess
import ykup
import checkConnection as check
import smbus
import RPi.GPIO as GPIO

# SAI SETUP

CLOCK_PIN = 27
PULSE_PIN = 22
BOUNCE_TIME = 30

i2c = smbus.SMBus(1)
sqwave = True
interrupted = False
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CLOCK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PULSE_PIN, GPIO.OUT, initial=sqwave)

def pwr_mode():
   data = i2c.read_byte_data(0x69, 0x00)
   data = data & ~(1 << 7)
   if (data == 1):
      return "EVC POWERED"
   elif (data == 2):
      return "SAI POWERED"
   else:
      return "ERROR"


def isr(channel):
	
	sqwave = not GPIO.input(PULSE_PIN)
	GPIO.output(PULSE_PIN, False)
	GPIO.setup(PULSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	if not GPIO.input(PULSE_PIN):
		# pin is low, this is shutdown signal from pico
		time.sleep(2)
		os.system('/app/PowerOff.sh')
	# change pulse pin back to output with flipped state
	GPIO.setup(PULSE_PIN, GPIO.OUT, initial=sqwave)
	power = pwr_mode()
	global interrupted
	if (power == "SAI POWERED"):
		print "Lost power suply, system will turn off"
		interrupted = True
	if (power == "EVC POWERED") and ( interrupted == True):
		print "Power supply recovered, system will reboot"
		interrupted = False
		os.system('/app/Reboot.sh')

GPIO.add_event_detect(CLOCK_PIN, GPIO.FALLING, callback=isr, bouncetime=BOUNCE_TIME)





#time.sleep(10)
usbPort=check.check()
if usbPort == 1:
    print("USB connected to Raspberry")
else:
    print("USB connected to EVC")
    ykup.RPI()
time.sleep(40)#Espera a que el EVC esté preparado(>1,5min)
ykup.EVC()
time.sleep(300)#Espera a que la descarga esté completa (>10 min)
ykup.RPI()
if os.path.isdir('/media/usb1/DRU')==True:
    for basename in os.listdir('/media/usb1/DRU'):
        if basename.endswith('.adru'):
            pathname = os.path.join('/media/usb1/DRU/', basename)
            if os.path.isfile(pathname):
                shutil.move(pathname,'/media/usb1/to_send/'+basename)
    subprocess.call(['/app/load_data_1.sh'])#LLama al bash para enviar los datos
elif os.path.isdir('/media/usb2/DRU')==True:
    for basename in os.listdir('/media/usb2/DRU'):
        if basename.endswith('.adru'):
            pathname = os.path.join('/media/usb2/DRU/', basename)
            if os.path.isfile(pathname):
                shutil.move(pathname,'/media/usb2/to_send/'+basename)
    subprocess.call(['/app/load_data_2.sh'])#LLama al bash para enviar los datos
else:
    print('DRU not founded')

while True:
	print ("ok")
	time.sleep(10)

##--------------to be deleted after test--------------
#import time
#import switchPort as switch

#a=0
#while a <=10:
#    switch.switch()
#    a=a+1
#    #time.sleep(1000)

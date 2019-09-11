#!/bin/bash
if [ -e /dev/sda1 ]
then
mkdir -p /media/usb1 && mount /media/usb1
echo usb1 mounted
fi
if [ -e /dev/sdb1 ]
then
mkdir -p /media/usb2 && mount /media/usb2
echo usb2 mounted
fi
if [ -e /dev/sdc1 ]
then
mkdir -p /media/usb1 && mount /media/usb3
echo usb3 mounted
fi
if [ -e /dev/sdd1 ]
then
mkdir -p /media/usb1 && mount /media/usb4
echo usb4 mounted
fi
udevadm control --reload-rules
python3.5 /app/power.py
exit 0
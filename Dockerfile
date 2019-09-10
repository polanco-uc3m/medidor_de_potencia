## ALSTOM SIGNAILLING SPAIN
# MV 49: CUSTOMER CARE
# Author Antonio Polanco Belmonte
# April 2019
#-------------------------------------------------------------------------------
# APP DOCKERFILE
# Docker Contanier configuration file.
# It manages dependencies, and initial procedures to set the DRU_data_extractor App
#------------------------------------------------------------------------------- 
FROM balenalib/raspberrypi3-node:10-stretch-run

# Enable UDEV
ENV UDEV=1

RUN echo /dev/sda1	/media/usb1	vfat	defaults,user,umask=002,nofail,utf8	0	0 >> /etc/fstab
RUN echo /dev/sdb1	/media/usb2	vfat	defaults,user,umask=002,nofail,utf8	0	0 >> /etc/fstab
RUN echo /dev/sdc1	/media/usb3	vfat	defaults,user,umask=002,nofail,utf8	0	0 >> /etc/fstab
RUN echo /dev/sdd1	/media/usb4	vfat	defaults,user,umask=002,nofail,utf8	0	0 >> /etc/fstab


# Install Packages.
RUN apt update \
	#&& apt-get install cron \
	&& apt-get install -y i2c-tools \
	&& apt-get install -y python \
	&& apt-get install python-rpi.gpio \
	&& apt-get install curl \
	&& apt-get install dbus \
	&& apt-get install python-smbus i2c-tools \
	# Remove package lists to free up space
	&& rm -rf /var/lib/apt/lists/*

# copy current directory into /app
COPY . /app

# overwrite udev rules
COPY 11-media-usb-mount.rules /etc/udev/rules.d/

# Make directories to manage data
RUN mkdir to_send
RUN mkdir sent_data

# Set Cronjobs
#RUN crontab /app/cronjobs
#RUN service cron restart

# Give permissions
RUN chmod 777 app/load_data_1.sh
RUN chmod 777 app/load_data_2.sh
RUN chmod +x /app/start.sh
RUN chmod +x /app/PowerOff.sh
RUN chmod +x /app/Reboot.sh

# run python script when container lands on device

CMD modprobe i2c-dev && /app/start.sh

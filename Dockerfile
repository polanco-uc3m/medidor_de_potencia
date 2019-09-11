# Author Antonio Polanco Belmonte

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
	&& apt-get install python-serial \
	&& apt-get install -y i2c-tools \
	&& apt-get install -y python3.5 \
	# Remove package lists to free up space
	&& rm -rf /var/lib/apt/lists/*

# copy current directory into /app
COPY . /app

# overwrite udev rules
COPY 11-media-usb-mount.rules /etc/udev/rules.d/

# Make directories to manage data

# Give permissions
RUN chmod +x /app/start.sh
RUN chmod +x /app/PowerOff.sh
RUN chmod +x /app/Reboot.sh

# run python script when container lands on device

CMD /app/start.sh

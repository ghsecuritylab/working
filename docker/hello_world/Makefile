#
# This is a project Makefile. It is assumed the directory this Makefile resides in is a
# project subdirectory.
#

PROJECT_NAME := hello-world

include $(IDF_PATH)/make/project.mk


build:
	sudo docker build --rm -t esp32 .

esp32_j5:
	 docker run \
	--device=/dev/ttyUSB0 \
	-v ${shell pwd}:/home/app \
	-it esp32 \
	make -j5 flash monitor # execute the build load the project to the chip and show monitor

esp32:
	 docker run \
	--device=/dev/ttyUSB0 \
	-v ${shell pwd}:/home/app \
	-it esp32 \
	make flash monitor # execute the build load the project to the chip and show monitor


esp32_monitor:
	 docker run \
	--device=/dev/ttyUSB0 \
	-v ${shell pwd}:/home/app \
	-it esp32 \
	make monitor # execute the build load the project to the chip and show monitor

esp32_bash:
	 docker run \
	--device=/dev/ttyUSB0 \
	-v ${shell pwd}:/home/app \
	-it esp32

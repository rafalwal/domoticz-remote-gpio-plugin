# domoticz-remote-gpio-plugin 
Plugin for read and set raspberry GPIOs from Domoticz on remote machine

Tested on Raspberry PI3 and PC with Domoticz on Debian system

This plugin is a modification of a plugin created by dnpwwo https://github.com/dnpwwo/Domoticz-GPIO-Plugin

On the Raspberry PI:
- enable remote GPIO in settings (Raspberry Pi configuration tool in menu)
- set selected GPIOs as OUTPUT
  e.g. (insert linie in some raspberry startup script)
    gpio mode 19 out  
  
- install pigpiod daemon:
    sudo apt update
    sudo apt install pigpio
    sudo systemctl enable pigpiod
    sudo systemctl start pigpiod
 
 On the computer with Domoticz:
 - install Python libraries
    sudo apt-get update
    sudo apt-get install pigpio python-pigpio python3-pigpio

- create folder RemoteGPIO in Domoticz/plugins
- insert file plugin.py into created folder
- restart domoticz

Configuration:
- Remote RPi IP address e.g 192.168.1.10
- Output Pins - Comma delimited list of output (relay) pins. Format is pin number colon NO or NC (e.g 39:NO or 39:NO,17:NC,19:NO)
- Heartbeat Frequency - Determines how often Input Pins are checked for values
- Debug - When true the logging level will be much higher to aid with troubleshooting
   
 Devices are created automatically.

 GPIO values may be change via another process or device. Plugin read actual state via Heardbeat
- NO - normal open - switch in domoticz device to 1 -> set GPIO to 1
- NC - normal closed - switch domoticz device to 1 -> set GPIO to 0
 
 NC is used by me for relay modulue switched on with logical zero.

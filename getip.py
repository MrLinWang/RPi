#!/usr/bin/python3
import socket
import struct
import fcntl

#def get_ip(ifname):
 #   s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',bytes(ifname[:15],'utf-8')))[20:24])

def get_ip(ifname):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',bytes(ifname[:15],'utf-8')))[20:24])

#print(get_ip('wlan0'))
 print(get_ip('0'))          
                            
                            

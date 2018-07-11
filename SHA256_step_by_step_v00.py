import numpy as np
import hashlib

message = ''

message_bin = bytes(message.encode('utf-8'))

myhash = hashlib.sha256(message_bin).hexdigest()

sep = '//'

cint = lambda st:''.join(format(ord(x), 'b') for x in st)

print(message,sep,message_bin,sep,myhash)

print(cint('Hallo'))
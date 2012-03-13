#! /usr/bin/env python
import sys
import socket
import unittest
import meep_example_app
import urllib
import datetime
import signal

e = {}
outputStatus = ''
outputHeaders = []

def parse_Serv(l):
    global e
    parts = l.split()
    e['Req_method'] = parts[0]
    if len(parts) > 2:
        e['Server_prot'] = parts[2]
    
    if parts[1].find('?') == -1:
        e['Path_Info'] = parts[1]
    else:
        url = parts[1].split('?')
        e['Path_info'] = url[0]
        e['Query_String'] = url[1]

def c(l):
    values = l.split(': ')[1]
    types = values.split(',')
    e['Content_type'] = types[0]

def parse_hosts:
    values = l.split(': ')[1]
    parts = values.split(':')
    e['Server_name'] = parts[0]
    if len(parts) > 1:
        e['Server_port'] = parts[1]

def parse_cook(l):
    e['Http_cookie'] = l.split(': ')[1]

def parse_http(l):
try:
key,value = l.split(': ')
key = 'HTTP_%s' % (key.upper().replace('-','_'),)
e[key] = value
except:
pass

def fake_response(status, headers):
global outputStatus, outputHeaders
outputStatus = status
outputHeaders = headers

def process_incoming(data,ip,port):

global e,outputStatus, outputHeaders

#LOAD DEFAULTS
e['Script_name'] = ''
e['Req_method'] = 'GET'
e['Path_Info'] = '/'
e['Query_String'] = ''
e['Server_prot'] = 'HTTP/1.1'
e['Server_name'] = socket.gethostbyaddr("69.59.196.211")
e['Server_port'] = str(port)
e['Content_type'] = 'text/plain'
e['Content_length'] = '0'
e['Http_cookie'] = ''

lines = data.splitlines()
for l in lines:
if l.startswith('Get'):
parse_Serv(l)
e['Content_length'] = '0'
elif l.lower().startswith('accept:'):
parse_Content_type(l)
elif l.lower().startswith('host:'):
parse_hosts
elif l.lower().startswith('cookie'):
parse_cook(l)
else:
parse_http(l)

print 'processed headers:'
for val in e:
print ' %s: %s' % (val,e[val],)

app = meep_example_app.MeepExampleApp()
print 'processing'
data = app(e, fake_response)
output = '%s %s\r\n' % (e['Server_prot'], outputStatus)
output += 'Date: %s EST\r\n' % datetime.datetime.now().strftime("%a, %d %b %Y %I:%M:%S")
output += 'Serv: HaydensAwesomeServer/0.1 Python/2.5\r\n'
output += 'Content-type: %s\r\n' % (e['Content_type'],)
output += 'Loc: %s\r\n' % (e['Path_info'],)
if len(data) > 0:
output += 'Content-Length: %d\r\n\r\n' % (len(data[0]),)
output += data[0]
else:
output += 'Content-Length: 0\r\n\r\n'
print 'done'
return output

def handle_connection(sock):
    while 1:
        try:
            data = sock.recv(4096)
            if not data:
                break
                    
            print 'data received from Internet protocol: ', (sock.getsockname(),)
            ip,port = sock.getsockname()
            sock.sendall(process_incoming(data, ip, port))
            sock.close()
            break
        except socket.error:
            print 'error'
            break

if __name__ == '__main__':
interface, port = sys.argv[1:3]
port = int(port)


print 'binding', interface, port
sock = socket.socket()
sock.bind( (interface, port) )
sock.listen(5)


while 1:
print 'waiting...'
(client_sock, client_address) = sock.accept()
print 'connection', client_address
handle_connection(client_sock)

sock.close()

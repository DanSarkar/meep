 e['PATH_INFO'] = '/'

   e['QUERY_STRING'] = ''

   e['SERVER_PROTOCOL'] = 'HTTP/1.1'

-  e['SERVER_NAME'] = socket.gethostbyaddr("69.59.196.211")

+  e['SERVER_NAME'] = socket.gethostbyaddr(ip)

   e['SERVER_PORT'] = str(port)

   e['CONTENT_TYPE'] = 'text/plain'

   e['CONTENT_LENGTH'] = '0'

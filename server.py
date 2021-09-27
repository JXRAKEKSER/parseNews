import socket
import sys
import json
import index;

MAX_LENGTH = 64*1024;
MAX_HEADERS = 100;
class Request:
  def __init__(self, method, target, protocolVersion, headers):
    self.__method = method;
    self.__target = target;
    self.__protocolVersion = protocolVersion;
    self.__headers = headers;

  def getTarget(self):
    return self.__target;

class Response:

  def __init__(self, status, reason, headers=None, body=None):
    self.status = status
    self.reason = reason
    self.headers = headers
    self.body = body

  def getHeaders(self):
    return self.headers;

  def getBody(self):
    return self.body;

class MyHTTPServer:
  def __init__(self, host, port, server_name):
    self._host = host
    self._port = port
    self._server_name = server_name

  def serve_forever(self):
    serv_sock = socket.socket(
      socket.AF_INET,
      socket.SOCK_STREAM,
      proto=0)

    try:
      serv_sock.bind((self._host, self._port))
      serv_sock.listen()
      print('Server start on port 5010');
      while True:
        conn, _ = serv_sock.accept()
        try:
          self.serve_client(conn)
        except Exception as e:
          print('Client serving failed', e)
    finally:
      serv_sock.close()

  def serve_client(self, conn):
    try:
      req = self.parse_request(conn)
      resp = self.handle_request(req)
      self.send_response(conn, resp)
    except ConnectionResetError:
      conn = None

    except Exception as e:
      self.send_error(conn, e)


    if conn:
      conn.close()

  def parse_request(self, conn):
    file = conn.makefile('rb');
    method, target , httpVer = self.parse_requestLine(file);
    headers = self.parse_headers(file);

    return Request(method, target, httpVer, headers);

  def parse_requestLine(self, file):

    byteStream  = file.readline(MAX_LENGTH +1);
    if(len(byteStream) > MAX_LENGTH):
      raise Exception('It\'s too long request line' );
    requestLine = str(byteStream, 'iso-8859-1');
    requestLine = requestLine.rsplit('\r\n')[0];
    requestLineList = requestLine.split();
    if(len(requestLineList) != 3):
      raise Exception('It\'s strange request line, it has {len(requestLineList)} length');
    method, target, httpVer = requestLineList;
    if(httpVer != 'HTTP/1.1'):
      raise Exception('Your HTTP version is surprised');
    return requestLineList;

  def parse_headers(self, file):
    headers = [];

    while True:
      byteStream = file.readline(MAX_LENGTH + 1);
      if(len(byteStream) > MAX_LENGTH):
        raise Exception('Headers too many long');

      if byteStream in b'\r\n':
        break;
      headers.append(byteStream);
      if(len(headers) > MAX_HEADERS):
        raise Exception('You have too many headers');
    headersDict = {}
    for header in headers:
      header = header.decode('iso-8859-1');
      key, value = header.split(':', 1);
      headersDict[key] = value;
    return headersDict;

  def get_handler(self, req):
    index.refreshNews();

    for item in index.getAllData():
      body = json.dumps(item);
    body = body.encode('utf-8');
    headers = [('Content-Type', 'application/json; charset=utf-8'),
               ('Content-Length', len(body)),
               ('Access-Control-Expose-Headers', 'Access-Control-Allow-Origin'),
               ('Access-Control-Allow-Origin', 'http://localhost:63342')]
    return Response(200, 'OK', headers, body);

  def handle_request(self, req):
    if(req.getTarget() == '/request'):
      return self.get_handler(req);

  def send_response(self, conn, resp):
    wfile = conn.makefile('wb')
    status_line = 'HTTP/1.1 {resp.status} {resp.reason}\r\n'
    wfile.write(status_line.encode('iso-8859-1'))

    if resp.getHeaders():
      for (key, value) in resp.getHeaders():
        header_line = '{key}: {value}\r\n'
        wfile.write(header_line.encode('iso-8859-1'))

    wfile.write(b'\r\n')

    if resp.getBody():
      wfile.write(resp.getBody())

    wfile.flush()
    wfile.close()

  def send_error(self, conn, err):
    pass  # TODO: implement me


if __name__ == '__main__':
  host = '127.0.0.1'
  port = int(50010)
  name = 'server.local'

  serv = MyHTTPServer(host, port, name)
  try:
    serv.serve_forever()
  except KeyboardInterrupt:
   pass
import socket
import threading

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 1501
ADDR = (SERVER,PORT)

httpserver = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
httpserver.bind(ADDR)

def GET_request():
    pass

def POST_request():
    pass

def send_response():
    pass

def handle_client(conn,addr):
    print(F"[NEW CONNECTION] {addr} connected")

    request = conn.recv(1024).decode('utf8')
    request_detail = request.split(' ')
    method = request_detail[0]
    requesting_file = request_detail[1]
    filename = requesting_file.split('?')[0]
    filename = filename.lstrip('/')
    if(filename ==''):
        filename = 'index.html'
    try:
        if(method == "POST"):
            request_body = request_detail[-1].split('\n')
            username = request_body[2].split('&')[0].split('=')[1]
            password = request_body[2].split('&')[1].split('=')[1]
            if(username != 'admin' or password != 'admin'):
                raise
        if(filename == "info.html" and method == "GET"):
            raise
        file = open(filename,'rb') 
        response = file.read()
        file.close()

        header = 'HTTP/1.1 200 OK\n'
  
        if(filename.endswith(".jpg")):
            mimetype = 'image/jpg'
        elif(filename.endswith(".css")):
            mimetype = 'text/css'
        else:
            mimetype = 'text/html'
    
        header += 'Content-Type: '+str(mimetype)+'\n\n'
    
    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><center><b><h1>404</h1><h3>Page not found</h3></b></center></body></html>'.encode('utf-8')
    final_response = header.encode('utf-8')
    final_response += response
    conn.send(final_response)
    conn.close()
    print("[DISCONNECT] {addr} has disconnected")


def start():
    httpserver.listen(10)
    print(f"[LISTENING] Server is listening on {ADDR}...")
    while True:
        conn, addr = httpserver.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()

print("[STARTING] Waiting for client...")
start()
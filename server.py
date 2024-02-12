import socket
import sys

def run_server(port):
    host = 'localhost'

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    while True:
        client_socket, client_address = server_socket.accept()
        # asking for a request from the client, and convert it to string
        request = client_socket.recv(1024).decode('utf-8')
        print('this is the request:\n' + request + '\n')


        if request:
            parsed_request = request.split()

            if len(parsed_request) >= 2 and parsed_request[0] == 'GET':
                file_path = parsed_request[1][1:]  # Remove the leading '/'
                if file_path == '' or file_path.endswith('/'):
                    file_path = 'index.html'

                if file_path == 'redirect':
                    file_path = 'result.html'

                try:
                    with open(file_path, 'rb') as file:
                        content = file.read()
                        if file_path == 'result.html':
                            http_response = f"""HTTP/1.1 301 Moved Permenentaly
Connection: close
Location: /result.html

"""
                        else:
                            http_response = f"""HTTP/1.1 200 OK
Connection: {parsed_request[6]}
Content-Length: {len(content)} 
                    
{content.decode('utf-8')}
"""
                
                except FileNotFoundError:
                    http_response = """HTTP/1.1 404 Not Found
Connection: close
"""

                except UnicodeDecodeError:
                    # Handle non-UTF-8 encoded content
                    http_response = f"""HTTP/1.1 200 OK
Content-Type: application/octet-stream

"""
                print('response of the server:\n' + http_response + '\n')
                client_socket.sendall(http_response.encode('utf-8'))

                # If it's a 404 response, close the connection
                if "404 Not Found" in http_response:
                    client_socket.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python server.py <port>')
        sys.exit(1)

    port = int(sys.argv[1])
    run_server(port)
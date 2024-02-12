import socket
import sys

def run_server(port):
    host = 'localhost'

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    # print(f'Server is running on http://{host}:{port}/')

    while True:
        client_socket, client_address = server_socket.accept()
        request = client_socket.recv(1024).decode('utf-8')
        print(request)

        if request:
            parsed_request = request.split()

            if len(parsed_request) >= 2 and parsed_request[0] == 'GET':
                file_path = parsed_request[1][1:]  # Remove the leading '/'

                if file_path == '' or file_path.endswith('/'):
                    file_path = 'index.html'

                try:
                    with open(file_path, 'rb') as file:
                        content = file.read()
                    http_response = f"""HTTP/1.1 200 OK
Content-Type: text/html

{content.decode('utf-8')}
"""
                except FileNotFoundError:
                    http_response = """HTTP/1.1 404 Not Found
Content-Type: text/html
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



############################################################






##########################################################



# import socket
# import sys

# def run_server(port):
#     host = 'localhost'

#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((host, port))
#     server_socket.listen(5)

#     while True:
#         client_socket, client_address = server_socket.accept()
#         request = client_socket.recv(1024).decode('utf-8')
#         print(request)

#         if request:
#             parsed_request = request.split()

#             if len(parsed_request) >= 2 and parsed_request[0] == 'GET':
#                 file_path = parsed_request[1][1:]  # Remove the leading '/'

#                 if file_path == '' or file_path.endswith('/'):
#                     file_path = 'index.html'

#                 try:
#                     with open(file_path, 'rb') as file:
#                         content = file.read()
#                     http_response = f"""HTTP/1.1 200 OK\nContent-Type: text/html\n\n{content.decode('utf-8')}"""
                    
#                 except FileNotFoundError:
#                     http_response = """HTTP/1.1 404 Not Found\nContent-Type: text/html"""
                    
#                 except UnicodeDecodeError:
#                     # Handle non-UTF-8 encoded content
#                     http_response = f"""HTTP/1.1 200 OK\nContent-Type: application/octet-stream"""
                    
#                 print('response of the server:\n' + http_response)
#                 client_socket.sendall(http_response.encode('utf-8'))

#         client_socket.close()

# if __name__ == '__main__':
#     if len(sys.argv) != 2:
#         print('Usage: python server.py <port>')
#         sys.exit(1)

#     port = int(sys.argv[1])
#     run_server(port)
import os
import socket
import sys
import os.path
from os import path

def handle_client(data, client_socket):
    connection = ""
    dont_keep_alive = True
    keep_alive = False
    messages_from_client = data.split("\r\n\r\n")

    for message in messages_from_client:
        if message.strip():
            first_line = message.partition("\r\n")[0]
            # print("this is first line: ", first_line)
            split_line = first_line.split(" ")
            # print("split_line is: ", split_line)

            if len(split_line) >= 2:
                my_path = "files" + split_line[1]

                # handles with redirect path
                if my_path == "files/redirect":
                    client_socket.send(
                        "HTTP/1.1 301 Moved Permanently\r\nConnection: close\r\nLocation: /result.html\r\n\r\n".encode())
                    return dont_keep_alive
                
                # checks if the file exists
                if path.exists(my_path):
                    if my_path[-1:] == "/":
                        my_path += "index.html"
                    length = os.stat(my_path).st_size
                    # finds a line with "Connection:"
                    for line in data.split("\r\n"):
                        if "Connection:" in line:
                            connection = line.split(" ")[1]
                            break

                    if connection == "close":
                        # print("inside connection=close")
                        return dont_keep_alive

                    message = f"HTTP/1.1 200 OK\r\nConnection: {connection}\r\nContent-Length: {length}\r\n\r\n"
                    file = open(my_path, "rb")
                    binary = file.read()
                    file.close()

                else:
                    client_socket.send("HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n".encode())
                    # print("inside keep_alive = False bevause in 404")
                    return dont_keep_alive
                
                # sends complete message to client
                client_socket.send(message.encode() + binary)
                return keep_alive

            else:
                # Handle the case where the split doesn't produce enough elements
                print("Error: Unable to extract the second element from the first line.")
                break


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCP_PORT = int(sys.argv[1])
    server.bind(('localhost', TCP_PORT))
    server.listen(1)
    while True:
        data = ""
        close_connection = False
        client_socket, client_address = server.accept()
        while not close_connection:
            client_socket.settimeout(1) # close the socket if timeout (in 1 sec) - that happenes if we don't recieve data from client
            try:
                received_data = client_socket.recv(1024).decode()
                # closes the socket when received an empty message
                if len(received_data) == 0:
                    client_socket.close()
                    break
                data += received_data

                # seperates between the data (messages) that was recieved from client
                messages_from_client = data.split("\r\n\r\n")
                
                for message in messages_from_client:
                    print(message) # prints the message from client
                    print() # prints an empty line to seperate between the messages
                    close_connection = handle_client(message, client_socket)
                    if close_connection == True: # in case of 404 or 301
                        # print("closing immediately the connectionnnnnn with client")
                        break

                # finished to recieve messages from client or 301/404
                client_socket.close()
                close_connection = True

            except socket.timeout as e:
                client_socket.close()
                break


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 server.py <port_number>')
        sys.exit(1)
    main()

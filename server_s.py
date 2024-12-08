# Transmission Control Protocol
# Library includes functions - interface for API sockets Berkeley
import socket

def main():
    # Creating a socket
    # AF_INET - using the IPv4(Internet Protocol version 4) - standalone specification
    # Host(server) is represented by IPv4 adress
    # And port(client) is an integer
    # SOCK_STREAM - supporting TCP - the connection is established
    # And server and client have a "conversation" until the connection
    # Is terminated by one of them or network error
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Binding socket to the adress
    # Localhost - IP adress from a local computer
    # And also from port 12345
    server_socket.bind(('localhost', 12345))
    # Starting to listen
    # 1 - max one connection
    server_socket.listen(1)

    print("Server is ready,awaiting the connection...")

    # Making the connection - accept() - waiting for the client
    # New socket for the conversation - conn
    # addr - client's address
    conn, addr = server_socket.accept()
    # f - special string format - to include {addr} immidiately
    print(f"The connection is established with {addr}")

    # Cycle for processing the messages
    while True:
	# Recovering max 1024 bytes from the conn socket
	# Decoding it from bytes to string
        data = conn.recv(1024).decode()
	# If empty(client broke the connection) - breaking the cycle
        if not data:
            break

        print(f"Got the message: {data}")

 	# Checking the message
        if data == "ping":
            response = "pong"
	    # Sending the response to the socket and encoding it into bytes
            conn.sendall(response.encode())
        else:
            break

    # Got the message, responded - closing the socket
    conn.close()
    # Closing the server's socket - to clear space
    server_socket.close()

if __name__ == "__main__":
    main()

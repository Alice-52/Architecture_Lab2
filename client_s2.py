# Transmission Control Protocol
# Library includes functions - interface for API sockets Berkeley
import socket
# Handling the exceptions - exiting
import sys
# For the wait in retrying to connect
import time


def main():
    # Defining the server's adress and port
    host = 'localhost'
    port = 2024

    while True:
        # Clearing it at first
        client_socket = None
        try:
            # Creating a TCP socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connecting it to the server at a certain address and port
            client_socket.connect((host, port))

            # Get the first-ensuring message from the server
            response = client_socket.recv(1024).decode()

            # If the server is busy, print a message and terminate the client
            if response == "The server is busy. Please try again later.":
                print(response)
                # Close the connection
                client_socket.close()
                # Exit the client
                break

            print(f"Connected to the server {host}:{port}.")

            # If the server is not busy, continue communication - entering the loop
            while True:
                try:
                    # Request from the user to input a message
                    message = input(
                        "Enter a message (for example, 'ping' for request or 'exit' to quit): "
                    ).strip()

                    # Check if the received message is empty
                    if not message:  # If the user entered an empty string
                        print("Empty message is not allowed. Please try again.")
                        continue

                    # Check if the user wants to exit the client
                    if message.lower() == "exit":
                        print("Exiting the client.")
                        client_socket.close()
                        sys.exit(0)

                    # Sending the user's message to the server - encoded
                    client_socket.sendall(message.encode('utf-8'))
                    print(f"Message sent to the server: {message}")

                    # Receiving a response
                    response = client_socket.recv(1024).decode('utf-8')

                    # Check for a zero response indicating a possible server disconnection
                    if not response:
                        print("Received an empty response from the server. It may be disconnected.")
                        # Exit the communication loop
                        break

                    print(f"Response from server: {response}")

                # Exceptions
                except socket.error as e:
                    # Obvious handling of send/receive data errors
                    print(f"Error while sending/receiving data: {e}")
                    # Break to exit the communication loop
                    break

        except socket.error as e:
            # Error while trying to connect
            print(f"Failed to connect to the server: {e}. Retrying in 5 seconds.")
            time.sleep(5)
        finally:
            if client_socket:
                client_socket.close()

# Ensure the main function runs when the script is executed
if name == "main":
    main()
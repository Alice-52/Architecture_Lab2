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
            # Connecting it to the server at a certain adress and port
	    client_socket.connect((host, port))

            # Get the first-ensuring message from the server
            response = client_socket.recv(1024).decode()

            # If the server is busy, print a message and terminate the client
            if response == "Server is busy. Please try again later.":
                print(response)
		# Close the connection
                client_socket.close()
		# Exit the client
                break

            print(f"Connected to server {host}:{port}.")

            # If the server is not busy, continue communication - entering the loop
            while True:
                try:
		    # Asking for the user to enter a message
                    message = input(
                        "Enter a message (e.g., 'ping' for a request or 'exit' to quit): "
                    ).strip()

		    # Checking if the user wants to exit the client
                    if message.lower() == "exit":
                        print("Terminating the client.")
                        client_socket.close()
                        sys.exit(0)

		    # Sending user's message to the client - encoded
                    client_socket.sendall(message.encode('utf-8'))
                    print(f"Message sent to server: {message}")

		    # Recieving the response
                    response = client_socket.recv(1024).decode('utf-8')

 		    # Check for a zero response indicating the server might be down
                    if not response:
                        print("Received an empty response from the server. It may be disconnected.")
                        # Exit the communication loop
			break


                    print(f"Response from server: {response}")

		# Exceptions
                except socket.error as e:
		    # Obviously, handling the send/recieve errors
                    print(f"Error during sending/receiving data: {e}")
		    # Breaking, to get out of the communication loop
                    break

        except socket.error as e:
	    # Error during tries to connect
            print(f"Failed to connect to server: {e}. Retrying in 5 seconds.")
            if client_socket:
		# Closing the socket, if it was created - for the retry
                client_socket.close()
	    # Waiting before retrying
            time.sleep(5)


# Ensure the main function runs when the script is executed
if __name__ == "__main__":
    main()

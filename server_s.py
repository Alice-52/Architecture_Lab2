# Transmission Control Protocol
# Library includes functions - interface for API sockets Berkeley
import socket
# Handling the exceptions - exiting
import sys
# Tracing errors for debugging
import traceback


# Function to process client connection
# conn - connection socket
# addr - client's adress
# active_clients - number of active connections
def handle_client(conn, addr, active_clients):
    try:
        # Client is ready
	# f - special string format - to include {addr} immidiately
        print(f"Client {addr} has connected.")

        # Sending ok to the client to confirm the connection
        # Encoding it to bytes
	conn.sendall("OK".encode())

        # Start an infinite loop to handle messages from the client
        while True:
            try:
                # Receive data from the client
        	# Recovering max 1024 bytes from the conn socket
        	# Decoding it from bytes to string in UTF-8 format(python standard)
                data = conn.recv(1024).decode('utf-8')

                # Check if the received message is empty
                if not data:
                    # If the message is empty, print a message and break the loop
                    print(f"Client {addr} sent an empty message. Closing the connection.")
                    break

                # Print the received message from the client
                print(f"Got this message from {addr}: {data}")

                # Check if the received message is "ping"
                if data.strip().lower() == "ping":
                    # Making the response
                    response = "pong"
                    # Send the encoded response back to the client
                    conn.sendall(response.encode())
                    # Print that the response has been sent
                    print(f"Responding to the {addr}: pong")
                else:
                    # If the message is not recognized, send an error message back to the client
                    conn.sendall("Incorrect. Awaited 'ping'.".encode())

            except socket.error as e:
                # Handle any socket-related errors that occur during message handling
                print(f"Error during message handling {addr}: {e}")
                break

    # Handling errors
    except Exception as e:
        # Catch any unexpected exceptions that occur while handling the client
        print(f"Error during client handling {addr}: {e}")

	# Print stack trace for debugging purposes
        traceback.print_exc()


    # Cleaning up everything
    finally:
        # Decrement the count of active clients to free up a slot for a new connection-client
        active_clients -= 1
        # Close the connection with the client to free resources
        conn.close()
        # Print a message indicating that the connection has been closed
        print(f"Connection with the client {addr} is closed.")


def main():
    # Creating a socket

    # Server is listening on the local machine - IP adress from a local computer
    host = 'localhost'
    # And also the port number where the server will accept connections
    port = 2024

    # The max amount of clients that server can handle
    number_of_clients = 1

    # To be sure of the amount of connected clients
    active_client = 0

    try:
        # Create a socket object using IPv4 and TCP
        # AF_INET - using the IPv4(Internet Protocol version 4) - standalone sp>    # Host(server) is represented by IPv4 adress
    	# And port(client) is an integer
    	# SOCK_STREAM - supporting TCP - the connection is established
    	# And server and client have a "conversation" until the connection
    	# Is terminated by one of them or network error
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set socket option to allow reusing the address
	# SOL_SOCKET - level of changing - only socket's options, not the protocol
	# SO_REUSEADDR - can bind to an address and port that are already in the TIME_WAIT state after another socket has closed
	# After shutting down - we can immediately bind to the same adress and port
	# 1 - enabling the option (0 - disable)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the host and port
        server_socket.bind((host, port))

        # Start listening for incoming connections
        # (_) - max connections
	server_socket.listen(numbers_of_clients)

	print(f"Server is ready and listening {port}.")

    # Error handling
    except socket.error as e:
        # Handle socket creation errors
        print(f"Error during the socket creation: {e}")
        # Exit the program if socket creation fails
	sys.exit(1)

    # Main loop to accept client connections
    while True:
        try:
            print("Waiting for the client to connect...")

            # Check if there's already an active client connection
            if active_client >= numbers_of_clients:

                # If the limit is reached, accept the connection but inform the client
                conn, addr = server_socket.accept()
                print(f"Client {addr} tried to connect, but this server is busy with another client.")
                conn.sendall("Server is busy. Try to connect later.".encode())
                # Closing this unused connection
		conn.close()
		# And continuing - waiting for new ones
                continue

            # Accept the incoming client connection
	    # Making the connection - accept() - waiting for the client
    	    # New socket for the conversation - conn
    	    # addr - client's address
            conn, addr = server_socket.accept()
            active_client += 1
	    # Calling special funciton
            handle_client(conn, addr, active_client)

	# Exceptions
        except KeyboardInterrupt:
            # Handle the interruption signal (like Ctrl+C)
            print("\nServer was stopped by the user.")
            # Breaking the loop to stop the server
	    break

	except OSError as e:
            # Handle operating system-related errors
            print(f"Error: maybe, port was closed: {e}")
            # Breaking the loop, because of the error
	    break

        except Exception as e:
            # Handle any other unexpected exceptions
            print(f"Unexpected error: {e}")
      	    # Print details of the exception for debugging
	    traceback.print_exc()
            # Breaking the loop, because of the error
	    break
	finally:
    	    # Clean up the mess and close the server socket
    	    server_socket.close()
    	    print("Server has shut down, sowy.")


# Ensure that the main function is called only when the script is executed directly
if __name__ == "__main__":
    main()

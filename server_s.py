# Transmission Control Protocol
# Library includes functions - interface for API sockets Berkeley
import socket
# Handling the exceptions, warnings
import logging
# For many clients at the same time
from threading import Thread

# Global variable to count active clients
active_clients = 0

# Function to handle client connection
# conn - connection socket
# addr - client's adress
def handle_client(conn, addr):
    # Indicate that we are working with a global variable
    global active_clients
    try:
        # Client is ready
	    # f - special string format - to include {addr} immidiately
        logging.info(f"Client {addr} connected.")
        # Sending ok to the client to confirm the connection
        # Encoding it to bytes
        conn.sendall("OK".encode())

        while True:
            try:
                # Receive data from the client
        	    # Recovering max 1024 bytes from the conn socket
        	    # Decoding it from bytes to string in UTF-8 format(python standard)
                data = conn.recv(1024).decode('utf-8')

                # Check if the received message is empty
                if not data:
                    # If the message is empty, print a message and break the loop
                    logging.warning(f"Empty message from {addr}. Connection closed.")
                    break

                # Print the received message from the client
                logging.info(f"Received from {addr}: {data}")

                # Check if the message is "ping"
                if data.strip().lower() == "ping":
                    # Making the response
                    response = "pong" 
                    # Send the encoded response back to the client
                    conn.sendall(response.encode()) 
                    # Print that the response has been sent
                    logging.info(f"Response sent to client {addr}: pong")
                else:
                    # If the message is not recognized, send an error message back to the client
                    conn.sendall("Invalid input. Expected 'ping'.".encode())

            except (ConnectionResetError, BrokenPipeError):
                # Handle connection errors
                logging.error(f"Connection error with {addr}. Connection closed.")
                break
            except socket.error as e:
                # Handle any socket-related errors that occur during message handling
                logging.error(f"Socket error with {addr}: {e}")
                break
    except Exception as e:
        # Handle any unexpected errors
        logging.exception(f"Unexpected error while handling client {addr}: {e}")

    finally:
        # Decrease the active clients counter and close the connection
        active_clients -= 1
        # Close the connection with the client to free resources
        conn.close()
        # Print a message indicating that the connection has been closed
        logging.info(f"Connection with client {addr} closed.")

# Main function to start the server
def main():
    # Indicate that we are working with a global variable
    global active_clients  

    # Set up logging
    # Level - of INFO and higher are tracked
    # %(asctime) - timestamp when the log message was created
    # %(levelname) - INFO, WARNING - level
    # %(message) - the message
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Server host and port
    # Server is listening on the local machine - IP adress from a local computer
    host = 'localhost'
    # And also the port number where the server will accept connections
    port = 2024
    # The max amount of clients that server can handle
    max_clients = 1
    server_socket = None 

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
        server_socket.listen(max_clients)  

        logging.info(f"Server started and listening on {host}:{port}")
        logging.info("Waiting for client connection...")
        while True:

            # Accept connection from a client
            conn, addr = server_socket.accept()

            # Check if the maximum number of connections has been reached
            if active_clients >= max_clients:
                logging.warning(f"Client {addr} tried to connect, but the server is busy.")
                conn.sendall("Server is busy. Please try later.".encode())
                conn.close()
                continue

            # Increase the active connections count
            active_clients += 1  
            # Create a new thread for the client
            # arg to provide to handle_client
            # Many clients in the same time
            Thread(target=handle_client, args=(conn, addr)).start()

    except OSError as e:
        # Log operating system errors
        logging.error(f"OS error: {e}")

    except Exception as e:
        # Log any unexpected errors
        logging.exception(f"Unexpected server error: {e}")

    finally:
        # Close the server socket if it was created
        if 'server_socket' in locals() and server_socket:
            # Close the socket to free resources
            server_socket.close() 
            # Log shutdown message 
            logging.info("Server shutting down.")  

# Entry point of the program
# Ensure that the main function is called only when the script is executed directly
if __name__ == "__main__": 
    main()

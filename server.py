# OS library - a portable way of using operating system dependent functionality
import os
# For time functions
import time


# Named channel
fifo = '/tmp/my_fifo'

# Making the path to channel, using os paths (FIFO)
# It allows one to send messages and the other one to read
if not os.path.exists(fifo):
    os.mkfifo(fifo)

def main():
    print("Server is ready. Waiting for messages...")
    # Launch the server to await message from client
    # True - while won't be stopped
    while True:
	# Opening the file - channel - for reading 
	# With - has exit logic after the code block will end
        with open(fifo, 'r') as fifo_file:
	    # Reading the message from the file
            message = fifo_file.read()
            if message == 'ping':
                print("Got the message: ping")
                # Sending the answer - writing in the file
                with open(fifo, 'w') as fifo_file:
                    fifo_file.write('pong')
	    # Shutting down
            else:
                print("Server shutting down.")
                break

# Checking if the file is actually the main programm
# And starting the main programm
if __name__ == "__main__":
    main()

# BenCommunication-Micropython-Server
A **python** library that runs on the server side to communicate with [BenCommunication-Micropython-client](https://github.com/blaze-Youssef/BenCommunication-Micropython-client).

The BenCommunication project uses UDP protocol to communicate with the [BenCommunication-Micropython-client](https://github.com/blaze-Youssef/BenCommunication-Micropython-client), it can assure a secure communication between Micropython and Python scripts over the network.
BenCommunication use AES CBC algorithm to encrypt the traffic with a key file that must be kept in a secure place.

**The library will:**

 - Generate a random iv for each request and send it along with the
   payload.
 - Generate a unique ID for each request.
## Installation
Download [benserver.py](link.com) and save it on the main directory of project.
Download requirements.txt and run :

    pip install -r requirements.txt


## Setup
Generate a keyfile using:

    from benserver import generate_new_secret
    generate_new_secret("key.sec")

## Object arguments
benserver.server() can have the following arguments:
 1. localip (str) => The IP the server is going to listen to, use "0.0.0.0".
 2. port (int) => The port used by server.
 3. keyfile (str) => (default=key.sec) the keyfile, it contains 32 random bytes. You can generate a key with the server module. 
 4. timeout (int) => (default=10) How much time to wait for response from server.
 5. buffersize (int) => (default=4096) The buffer for Udp Socket.
 
 ## Usage
 You can add functions to handle actions sent by [client](https://github.com/blaze-Youssef/BenCommunication-Micropython-client) with:
 

    from benserver import server
    udpserver = benServer("0.0.0.0",8585)
    def echo(text):
		return  text
	udpserver.add_action_handler("echo", echo) # When user send {"action":"echo","data":...}, it will return same data.
	udpserver.start() # Start listening for infinite time.
	

## Example receive data from sensor every 1 minute
See [Example to send data from sensor every 1 minute](https://github.com/blaze-Youssef/BenCommunication-Micropython-client#example-to-send-data-from-sensor-every-1-minute) 

		

 Last tested  with MicroPython v1.19.1 on 2022-06-18; ESP module with ESP8266.
 
**If you have any suggestions, feel free to fork and send a pull request.**
**Thanks for reading :D**
  


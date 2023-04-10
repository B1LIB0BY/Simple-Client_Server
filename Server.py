import socket
import threading
import time
import random
import requests

# Set up the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 0))
server_socket.listen()

# Get the server port and display it
server_port = server_socket.getsockname()[1]
print(f"Server listening on port {server_port}")

# Define a function to handle client connections
def handle_client(client_socket, address):
    print(f"New connection from {address}")
    while True:
        # Receive a message from the client
        message = client_socket.recv(1024).decode()
        if not message:
            break
        print(f"Received message from {address}: {message}")
        if message == "EXIT":
            break
        elif message.startswith("QUIT:"):
            password = message.split(":")[1]
            if password == "password":
                client_socket.send("QUIT command received".encode())
                break
            else:
                client_socket.send("Incorrect password".encode())
        elif message == "TIME":
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            client_socket.send(current_time.encode())
        elif message == "QUOTE":
            arr = ["'Happiness depends upon ourselves.' — Aristotle", "'Happiness is when what you think, what you say, and what you do are in harmony.' —Mahatma Gandhi",
                   "'The moments of happiness we enjoy take us by surprise. It is not that we seize them, but that they seize us.' — Ashley Montagu",
                   "'Even if happiness forgets you a little bit, never completely forget about it.' —Jaques Prevert",
                   "'One of the secrets of a happy life is continuous small treats.' —Iris Murdoch"]
            rannum = random.randint(0, len(arr)-1)
            client_socket.send(arr[rannum].encode())
        elif message == 'JOKE':
            url = "https://v2.jokeapi.dev/joke/Any"
            response = requests.get(url).json()
            if response["type"] == "single":
                joke = response["joke"]
            else:
                setup = response["setup"]
                delivery = response["delivery"]
                joke = f"{setup}\n{delivery}"
            client_socket.send(joke.encode())
        else:
            # Echo the message back to the client
            client_socket.send(message.encode())
    print(f"Closing connection from {address}")
    client_socket.close()

# Listen for client connections
while True:
    client_socket, address = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_socket, address)).start()

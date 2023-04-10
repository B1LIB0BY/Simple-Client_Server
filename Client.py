import socket
import tkinter as tk

# Set up the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(input("Enter the port that the server gave you: "))
client_socket.connect(("localhost", port))

# Get the server port and display it
server_port = client_socket.getpeername()[1]
print(f"Connected to server on port {server_port}")

# Get a password from the user
password = input("Enter password: ")

# Define a function to send messages to the server
def send_message(event=None):
    message = input_text.get("1.0", tk.END).strip()
    if message:
        if message == "EXIT":
            client_socket.send(message.encode())
            response = client_socket.recv(1024).decode()
            output_text.insert(tk.END, f"Server response: {response}\n")
            client_socket.close()
            root.destroy()
        elif message == f"QUIT:{password}":
            client_socket.send(message.encode())
            response = client_socket.recv(1024).decode()
            output_text.insert(tk.END, f"Server response: {response}\n")
            client_socket.close()
            root.destroy()
        elif message == "TIME":
            client_socket.send(message.encode())
            response = client_socket.recv(1024).decode()
            output_text.insert(tk.END, f"Server time: {response}\n")
        elif message == "QUOTE":
            client_socket.send(message.encode())
            response = client_socket.recv(1024).decode()
            output_text.insert(tk.END, f"Random Quote: {response}\n")
        else:
            client_socket.send(message.encode())
            response = client_socket.recv(1024).decode()
            output_text.insert(tk.END, f"Server response: {response}\n")
    input_text.delete("1.0", tk.END)

# Create a Tkinter window for the client
root = tk.Tk()
root.title("Client")
root.geometry("500x300")

# Create a text widget for the user to input messages
input_text = tk.Text(root, height=1)
input_text.pack(pady=5)

# Create a text widget to display messages from the server
output_text = tk.Text(root)
output_text.pack(fill=tk.BOTH, expand=True)

# Bind the send_message function to the Enter key
input_text.bind("<Return>", send_message)

# Create a button to send messages
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

# Start the Tkinter event loop
root.mainloop()


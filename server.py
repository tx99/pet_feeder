import socket
import pickle


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# dictionary to hold all the information on the pets
pets = {}


host = "0.0.0.0"
port = 9999
server_socket.bind((host, port))
# Up to five connection requests will be queued.
server_socket.listen(5)


# Function to add the pet data to the pets dictionary
def process_data(data):
    pets.update(pickle.loads(data))
    print(pets)

# Save pets data to file
def save_data():
    f = open("pets.pkl", 'wb')
    pickle.dump(pets, f)

    f.close()
# Load the pets data from a file
def load_data():
    f = open("pets.pkl", 'rb')
    pets.update(pickle.load(f))
    print(pets)
    f.close()


try:
    load_data()
except:
    print("pets.pkl does not exist or could not be read")

# infinte loop to wait for clients to download the pets data or for a new
# pet to be registered
while True:
    clientsocket, addr = server_socket.accept()
    print("Connection established from %s" % str(addr))

    # This code checks to see if a new pet has been registered
    message = clientsocket.recv(1024).decode('UTF-8')
    if (message == "new_pet"):
        process_data(clientsocket.recv(1024))
        save_data()

    # Send the pets data to the client
    data = pickle.dumps(pets)
    clientsocket.send(data)
    print("data sent to client.")

    # Close the clients connection and wait for the next one.
    clientsocket.close()


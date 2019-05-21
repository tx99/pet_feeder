#!/usr/bin/python3           # This is client.py file

import socket
import pickle
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Setup for the motion sensor
GPIO.setmode(GPIO.BCM)
PIR_PIN = 21
GPIO.setup(PIR_PIN, GPIO.IN)
LED_PIN = 15
GPIO.setup(LED_PIN, GPIO.OUT)


host = "192.168.100.78"
port = 9999


# dict for storing pet data
pets = {}

# The role is the door or food bowl the device will be opening
role = "t_bowl"


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

# Function to send pets data over the network
def send_pets(pet_dict):
    data = pickle.dumps(pet_dict)
    s.send(data)


# Function used to receive pets data over the network
def recv_pets(data):
    pets.clear()
    pets.update(pickle.loads(data))

# Function to send data over the network
def send_data(data):
    try:
        s.connect((host, port))
        s.send(data)
        s.close()
    except:
        print("Could not connect to server to send data.")

# Function to receive pet data from the server.s
def recv_data():
    try:
        s.connect((host, port))
        # This message is sent because the server expects to receive a message
        # with the data that will be sent.
        message = "null"
        s.send(message.encode('UTF-8'))
        data = s.recv(1024)
        s.close()
        recv_pets(data)
        save_data()
    except:
        print("Could not connect to server to receive data.")

        # Could not connect to server so the most recent local copy
        # of the pet data will be used.
        load_data()
        print("pet data loaded from backup")

# This function determins if the pet has permission to use that door/bowl.
# For the food bowls there is a motion sensor so that the food bowl remains open
# while motion is detected.
def process_permissions(name, gpio_pin):
    if (pets[name][role] == 'y'):
        print("permission for the ", role, " granted to ", name)

        # While permission is allowed use the motion sensor
        # to determine if the pet is still there so the food bowl
        # will not be closed.
        if GPIO.input(PIR_PIN) == True:
            print("Motion detected, food bowl will stay open")
            GPIO.output(LED_PIN, True)
            time.sleep(10)
            GPIO.output(LED_PIN, False)
        else:
            GPIO.output(LED_PIN, False)
    else:
        print(name, " attempted to access the ", role)

# on start connect to server and download the latest pet data
recv_data()

# Setup the RFID reader
reader = SimpleMFRC522()

GPIO.output(LED_PIN, False)
# infinite loop to wait for an RFID tag to be read
while True:
    print("Waiting for pet.")
    try:
        id, name = reader.read()
    except KeyError:
        print("Error, unable to read RFID tag. Please try again")
        quit = input("Stop client y/n: ")
        if (quit == 'y'):
            GPIO.cleanup()
            break
    process_permissions(name.rstrip(), PIR_PIN)


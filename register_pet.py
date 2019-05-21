import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import socket
import pickle

reader = SimpleMFRC522()

pet = {}
pets = {}

try:
    pet_name = input("Enter the pets name: ")
    kitchen_bowl = input("Give access to kitchen bowl y/n: ")
    main_bedroom = input("Give access to the main bedroom y/n: ")
    t_bowl = input("Give access to Tigra's bowl y/n: ")
    f_bowl = input("Give access to Fetitas bowl y/n: ")
    s_bowl = input("Give access to Sam's bowl y/n: ")

    print("Place the tag near the reader to get the ID")
    id = reader.read()
    print ("ID read successfully")

    # Create the pet dict
    pet["name"] = pet_name
    pet["id"] = id
    pet["kitchen_bowl"] = kitchen_bowl
    pet["main_bedroom"] = main_bedroom
    pet["t_bowl"] = t_bowl
    pet["f_bowl"] = f_bowl
    pet["s_bowl"] = s_bowl

    print(pet)
    pets.update({pet_name: pet})
    print(pets)
    print("Writing to RFID...Place the RFID tag near the reader.")
    reader.write(pet_name)

    test = input("Would you like to test the RFID tag? y/n: ")
    if (test == 'y'):
        print("place the RFID tag near the reader")
        print(reader.read())

    print("Sending the data to the server...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.100.78"
    port = 9999
    s.connect((host, port))
    s.send("new_pet".encode('UTF-8'))
    s.send(pickle.dumps(pets))

finally:
    GPIO.cleanup()

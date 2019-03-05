import pygame
import threading
import serial
import random
import os

pygame.mixer.init()

class myThread (threading.Thread):
    def __init__(self, audioFile):
        threading.Thread.__init__(self)
        self.audioFile = audioFile
    def run(self):
        arduinoSerialData.flushInput()
        pygame.mixer.music.load(audioFile)
        pygame.mixer.music.play()

# Define the IO serial data
arduinoSerialData = serial.Serial('/dev/ttyACM0', 9600)
audioPath = os.getcwd().replace("\\", "/") + "/audio/"

# Create new threads
thread1 = myThread('')
thread2 = myThread('')

while True :
    if(thread1.isAlive() == False or thread2.isAlive() == False) :
        if (arduinoSerialData.inWaiting()>0) :
            if (arduinoSerialData.readline()) :
                distance = int(arduinoSerialData.readline().decode('utf8'))
                if (distance < 20) :
                    audioFile = audioPath+random.choice(os.listdir(audioPath))
                    print(audioFile)
                    if(thread1.isAlive() == False) :
                        thread1 = myThread(audioFile)
                        thread1.start()
                    elif(thread2.isAlive() == False) :
                        thread2 = myThread(audioFile)
                        thread2.start()

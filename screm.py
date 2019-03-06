import pygame
import threading
import serial
import random
import os
import time

# define audio player and # of channels & path for audio files
pygame.mixer.init()
pygame.mixer.set_num_channels(100)
path = os.getcwd().replace("\\", "/") + "/audio/"

# define the IO serial data 
arduinoSerialData = serial.Serial('/dev/ttyACM0', 9600)

# range the bot will react, in cm
territory = 20
# minimum volume the bot will play (from 0.0 -> 1.0)
minVolume = 0.2
# how long the bot pauses between sounds
wait = 0.1

while True :
    if (arduinoSerialData.inWaiting()>0) :
        if (arduinoSerialData.readline()) :
            distance = int(arduinoSerialData.readline().decode('utf8'))
            
            if (distance < territory) :
                print('Something in range within', territory, ' cm!')
                
                file = path+random.choice(os.listdir(path))
                print('sound: '+file.split('/audio/',1)[1])
                
                absoluteVolume = str(1-distance/territory)
                volume = float(absoluteVolume[:absoluteVolume.find('.')+2])
                if (volume < minVolume) :
                    volume = minVolume
                print('volume: ', volume)
                
                audio = pygame.mixer.Sound(file)
                audio.set_volume(volume)
                if (pygame.mixer.find_channel()) :
                    channel = pygame.mixer.find_channel()
                    channel.queue(audio)
                
                print('')
                
    arduinoSerialData.flushInput()
    time.sleep(wait)
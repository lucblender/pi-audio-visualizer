import pygame
import pyaudio
import pygame.display
from time import sleep
from audio_decoder import AudioDecoder
import struct
import numpy
import collections
from pico_gpio_interface import PicoGpioInterface

import signal
import sys

display_type = 0
X = 720
Y = 720
black = (0, 0, 0)
white = (255, 255, 255)
pygame.init()
pygame.font.init()
pygame.mouse.set_visible(0)
display_surface = pygame.display.set_mode((X, Y ), pygame.FULLSCREEN)
dejavu_20 = pygame.font.SysFont('dejavusansmono', 20)

pico_gpios = PicoGpioInterface()

list_pot_R = collections.deque(maxlen=5)
list_pot_L = collections.deque(maxlen=5)

def avg_list(input_list):
    return sum(input_list) / len(input_list)

def custom_callback(in_data, frame_count, time_info, status):
    global display_surface, X, Y, display_type, old_data_L, old_data_R
    display_surface.fill(black)
    fmt = "%dH"%(len(in_data)/2)
    data_formatted = struct.unpack(fmt, in_data)
    data_formatted = numpy.array(data_formatted, dtype='h')    
    data_formatted = data_formatted[1::2] # one out of two sample = 0
    data_L = data_formatted[0::2]   # divide right and left channel
    data_R = data_formatted[1::2]
    #print("c", len(data_L), max(data_L), type(data_L))
    
    try:
        list_pot_R.append(pico_gpios.get_pot_0())
    except:
        list_pot_R.append(100)
    try:
        list_pot_L.append(pico_gpios.get_pot_1())
    except:
        list_pot_L.append(100)
    
    pot_factor_R = int(avg_list(list_pot_R))/100
    pot_factor_L = int(avg_list(list_pot_L))/100
       
    try:
        display_type = pico_gpios.get_btn_0()
    except:
        display_type = 0
    
    if display_type == 0:
        step = X/len(data_L)
        factor_L = 1/1024*Y*pot_factor_R
        factor_R = 1/1024*Y*pot_factor_L
        i = 0
        for i in range(0, len(data_L)-1):
            x_coord_L = (i*step,data_L[i]*factor_L+Y/2)
            y_coord_L = ((i+1)*step,data_L[i+1]*factor_L+Y/2)
            x_coord_R = (i*step,data_R[i]*factor_R+Y/2)
            y_coord_R = ((i+1)*step,data_R[i+1]*factor_R+Y/2)
            #print(x_coord, y_coord, i)
            pygame.draw.line(display_surface, (127, 10, 50), x_coord_R, y_coord_R, 5)
            pygame.draw.line(display_surface, (71, 47, 150), x_coord_L, y_coord_L, 5)
            i+=1
        pygame.display.update() 
    elif display_type == 1:
        """
        data_L_conc = numpy.empty(0)
        data_R_conc = numpy.empty(0)
        
            
        old_data_L.append(numpy.flip(data_L))
        old_data_R.append(numpy.flip(data_R))
        
        for old_sample_L in reversed(old_data_L):
            data_L_conc = numpy.concatenate((numpy.flip(old_sample_L),data_L_conc))
        for old_sample_R in reversed(old_data_R):
            data_R_conc = numpy.concatenate((numpy.flip(old_sample_R),data_R_conc))
        """
        
        step = X/len(data_L)
        factor_L = 1/1024*Y*pot_factor_L
        factor_R = 1/1024*Y*pot_factor_R
        i = 0
        for i in range(0, len(data_L)-1):
            x_coord = (data_L[i]*factor_L+Y/2,data_R[i]*factor_R+Y/2)
            y_coord = (data_L[i+1]*factor_L+Y/2,data_R[i+1]*factor_R+Y/2)
            light_factor = i/len(data_L)
            pygame.draw.line(display_surface, (255*light_factor, 74*light_factor, 219*light_factor), x_coord, y_coord, 5)
            i+=1
        pygame.display.update() 
        
    return in_data, pyaudio.paContinue

#ad = AudioDecoder()
ad = AudioDecoder(custom_callback)

display_surface.fill(white)
pygame.display.update() 

pygame.display.update() 
while(True):
    sleep(.5)


import pyaudio
import numpy
import math
import time

from os import system


# Microphone
CHUNK = 1024
FORMAT_USB = pyaudio.paInt32
CHANNELS_USB = 2
DEVICE_INDEX_USB = 1
MICRO_RATE = 48000
RECORD_SECONDS = 10


class AudioDecoder():

    def __init__(self, custom_callback=None):
        if custom_callback == None:
            custom_callback = self.callback
        time.sleep(.1)
        self.pa = pyaudio.PyAudio()
        self.stream_usb = self.pa.open(format=FORMAT_USB,
                channels=CHANNELS_USB,
                rate=MICRO_RATE,
                input=True,
                frames_per_buffer=CHUNK,
				input_device_index = DEVICE_INDEX_USB,
                stream_callback=custom_callback)
        self.last_time = time.time()
        
    def reset_audio(self):   
        self.stream_usb.close()
        self.pa.terminate()
        self.pa = pyaudio.PyAudio()
        
    def reset_stream(self):
        try:
            print("Reset")
            self.reset_audio()
            time.sleep(.1)
            self.stream_usb = self.pa.open(format=FORMAT_USB,
                    channels=CHANNELS_USB,
                    rate=MICRO_RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index = DEVICE_INDEX_USB,
                    stream_callback=self.callback)                    
            self.__noise_level = 0
            self.__timestamp = time.time()
            print("Stream re-opened")
            time.sleep(1)
        except Exception as e:
            print(str(e))
            return False
        else:
            return True

    def callback(self, in_data, frame_count, time_info, status):
        # default callback can help to debug
        print("a:", len(in_data), print(frame_count))
        print("b:",in_data[0], type(in_data[0]))
        tmp_time = time.time()
        print("c:",tmp_time-self.last_time)
        self.last_time = tmp_time
        return in_data, pyaudio.paContinue

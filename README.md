# pi-audio-visualizer

This repository contain the  code to make an audio visualizer with a raspberry pi.
The goal is to display either :
- The two audio channels in function of the time
- The two audio channels using lissajous curves

The raspberry pi is used to retreive and compute the audio. The raspberry pico is used to handle the potentiometer and button used as User interface. The two are using i2c to communicate.

## Requirment

### Software

- pyaudio
- pygame

### Hardware

- Pimori square hyperpixel or equivalent
- Any usb audio card

## Run the software

### Wiring 

- The raspberry pico I2C0 GP0 SDA & GP1 SDL need to be wired to the i2c-1 GPIO2 SDA GPIO3 SDL of the raspberry pi. 
- The Left-channel potentiometer is wired to the Analog input ADC0 of the pico.
- The Right-channel potentiometer is wired to the Analog input ADC1 of the pico.
- The Mode button is wired to the Digital input GP2 of the pico.

A screen need to be attached to the raspberry pi and a audio card too. The better sample rate the audio card has, the better the visualization will be.

### Rapsberry pico

The Raspberry pico needs to run uPython. The main.py is automatically launched at power up.

### Rapsberry pi Service

A service named audio_visualizer.service can be used to run the software on the raspberry pi



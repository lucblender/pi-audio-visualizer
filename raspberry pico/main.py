import machine
import utime
from machine import mem32
from i2cSlave import i2c_slave

btn_0 = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
btn_1 = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)
btn_2 = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)

analog_array = [0,0,0,0,0,0]
digital_array = [0,0,0]
analog_value_0 = machine.ADC(26)
analog_value_1 = machine.ADC(27)
analog_value_2 = machine.ADC(28)

def retrieve_analog():
    reading_0 = analog_value_0.read_u16()   
    reading_1 = analog_value_1.read_u16()   
    reading_2 = analog_value_2.read_u16()
    analog_array[0] = reading_0&0xff
    analog_array[1] = (reading_0>>8)&0xff
    analog_array[2] = reading_1&0xff
    analog_array[3] = (reading_1>>8)&0xff
    analog_array[4] = reading_2&0xff
    analog_array[5] = (reading_2>>8)&0xff
    
def retrieve_digital():
    digital_array[0] = btn_0.value()
    digital_array[1] =btn_1.value()
    digital_array[2] =btn_2.value()
    
if __name__ == "__main__":
    s_i2c = i2c_slave(0,sda=0,scl=1,slaveAddress=0x41)
    last_index = 0
    try:
        while True:
            if s_i2c.any():
                last_index = s_i2c.get()
                print(last_index)
            if s_i2c.anyRead():
                if last_index > 8:
                    s_i2c.put(0xff)
                elif last_index > 5:    
                    retrieve_digital() 
                    s_i2c.put(digital_array[last_index-6])  
                else:                    
                    retrieve_analog()
                    s_i2c.put(analog_array[last_index])
        
    except KeyboardInterrupt:
        pass

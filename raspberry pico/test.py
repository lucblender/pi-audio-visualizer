import machine
import utime
from machine import mem32
from i2cSlave import i2c_slave

analog_array = [0,0,0,0,0,0]
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

if __name__ == "__main__":
    s_i2c = i2c_slave(0,sda=0,scl=1,slaveAddress=0x41)
    last_index = 0
    try:
        while True:
            retrieve_analog()
            if s_i2c.any():
                last_index = s_i2c.get()
                print(last_index)
            if s_i2c.anyRead():
                if last_index > 5:
                    s_i2c.put(0xff)
                else:   
                    s_i2c.put(analog_array[last_index])
        
    except KeyboardInterrupt:
        pass

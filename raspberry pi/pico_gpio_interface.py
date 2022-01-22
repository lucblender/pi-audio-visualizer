import smbus

BUS = 22
ADDR_PICO = 0x41


class PicoGpioInterface():
    def __init__(self):
        self.bus = smbus.SMBus(BUS)
        
    def get_pot_0(self):
        self.bus.write_byte(ADDR_PICO, 0x00)
        lsb = self.bus.read_byte(ADDR_PICO)
        self.bus.write_byte(ADDR_PICO, 0x01)
        msb = self.bus.read_byte(ADDR_PICO)
        return int((lsb + (msb<<8))/65536*100)
        
    def get_pot_1(self):
        self.bus.write_byte(ADDR_PICO, 0x02)
        lsb = self.bus.read_byte(ADDR_PICO)
        self.bus.write_byte(ADDR_PICO, 0x03)
        msb = self.bus.read_byte(ADDR_PICO)
        return int((lsb + (msb<<8))/65536*100)
        
    def get_pot_2(self):
        self.bus.write_byte(ADDR_PICO, 0x04)
        lsb = self.bus.read_byte(ADDR_PICO)
        self.bus.write_byte(ADDR_PICO, 0x05)
        msb = self.bus.read_byte(ADDR_PICO)
        return int((lsb + (msb<<8))/65536*100)
        
    def get_btn_0(self):
        self.bus.write_byte(ADDR_PICO, 0x06)
        data = self.bus.read_byte(ADDR_PICO)
        return data
        
    def get_btn_1(self):
        self.bus.write_byte(ADDR_PICO, 0x07)
        data = self.bus.read_byte(ADDR_PICO)
        return data
        
    def get_btn_3(self):
        self.bus.write_byte(ADDR_PICO, 0x07)
        data = self.bus.read_byte(ADDR_PICO)
        return data
        

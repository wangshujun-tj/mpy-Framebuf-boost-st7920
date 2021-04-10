# MicroPython ST7920 LCD driver, SPI interfaces

from micropython import const
import framebuf
import time

class ST7920(framebuf.FrameBuffer):
    
    def __init__(self, width, height, spi, cs):
        
        self.width = width
        self.height = height
        self.buffer = bytearray(self.height * self.width//8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HLSB, self.width)
        self.write_buf = bytearray(3)
        cs.init(cs.OUT, value=1)
        self.spi = spi
        self.cs = cs
        self.cs(0)
        self.init_display()

    def init_display(self):
        self.write_cmd(0x30)
        self.write_cmd(0x03)
        self.write_cmd(0x0c)
        self.write_cmd(0x01)
        time.sleep_ms(2)
        self.write_cmd(0x36)

        
    def write_cmd(self, cmd):
        self.write_buf[0]=0xf8
        self.write_buf[1]=cmd&0xf0
        self.write_buf[2]=(cmd&0x0f)<<4
        self.cs(1)
        self.spi.write(self.write_buf)
        self.cs(0) 
        #time.sleep_us(72)

    def write_data(self, dat):
        self.write_buf[0]=0xfa
        self.write_buf[1]=dat&0xf0
        self.write_buf[2]=(dat&0x0f)<<4
        self.cs(1)
        self.spi.write(self.write_buf)
        self.cs(0)
        #time.sleep_us(72)
    def show(self):
        for page in range(2):
            for line in range(32):
                self.write_cmd(0x80+line)
                self.write_cmd(0x80+page*8)
                for byte in range(16):
                    #self.write_data(0x55)
                    self.write_data(self.buffer[page*512+line*16+byte])


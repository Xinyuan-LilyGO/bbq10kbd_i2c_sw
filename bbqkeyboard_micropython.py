from micropython import const
from machine import I2C,Pin
import utime


KEY_BOARD_ADDR = const(0x01F) #address of keyboard

VERSION = const(0x01) #version register 固件版本
CONOFIG = const(0x02) #config register 配置寄存器
INTERRUPT_STATUS = const(0x03) #interrupt status register 中断状态寄存器
KEY_STATUS = const(0x04) #key status register 键状态寄存器
BLACKLIGHT = const(0x05) #black light register  背光控制
DEBOUNCE = const(0x06) #debounce config 防反跳配置寄存器（无
POLL_FREQ = const(0x07)# poll frequency config 轮询频率（无
RESET= const(0x08) #reset 复位
FIFO = const(0x09) # fifo config register  fifo访问寄存器

WRITE_MASK = const(1<<7)

#config register
#default : CFG_OVERFLOW_INT | CFG_KEY_INT | CFG_USE_MODS
CFG_OVERFLOW_ON  = const(1 << 0) 
CFG_OVERFLOW_INT = const(1 << 1)
CFG_CAPSLOCK_INT = const(1 << 2)
CFG_NUMLOCK_INT  = const(1 << 3)
CFG_KEY_INT      = const(1 << 4)
CFG_PANIC_INT    = const(1 << 5)


#interrupt status register
# must reset to 0 after reading
INT_OVERFLOW     = const(1 << 0)
INT_CAPSLOCK     = const(1 << 1)
INT_NUMLOCK      = const(1 << 2)
INT_KEY          = const(1 << 3)
INT_PANIC        = const(1 << 4)

#key status register
KEY_CAPSLOCK     = const(1 << 5)
KEY_NUMLOCK      = const(1 << 6)
KEY_COUNT_MASK   = const(0x1F)

#fifo config register
STATE_IDLE       = const(0)
STATE_PRESS      = const(1)
STATE_LONG_PRESS = const(2)
STATE_RELEASE    = const(3)
'''
class bbqiic:
    def __init__(self):


'''        


class BBQ10Keyboard:
    def __init__(self,i2c):
        self.i2c = i2c
        self.i2c_buffer = bytearray(2)
        self.reset()
    def i2c_write(self,word):
        #with self.i2c as bbq_i2c:
        self.i2c.writeto(KEY_BOARD_ADDR,word)
    def i2c_read(self,buffer):
        #with self.i2c as bbq_i2c:
        self.i2c.readfrom_into(KEY_BOARD_ADDR, buffer)

    def reset(self):
        self.i2c_buffer[0] = RESET
        self.i2c_write(self.i2c_buffer)
        utime.sleep_ms(50)
    

    @property
    def status(self):
        self.i2c_buffer[0] = KEY_STATUS
        self.i2c_write(self.i2c_buffer)
        self.i2c_read(self.i2c_buffer)
        return self.i2c_buffer[0]

    @property
    def key_count(self):
        return self.status & KEY_COUNT_MASK

    @property
    def key(self):
        if self.key_count ==0:
            return None
        self.i2c_buffer[0] = FIFO
        self.i2c_write(self.i2c_buffer)
        self.i2c_read(self.i2c_buffer)
        return (int(self.i2c_buffer[0]),chr(self.i2c_buffer[1]))


    @property
    def blacklight(self):
        self.i2c_buffer[0] = BLACKLIGHT
        self.i2c_write(self.i2c_buffer)
        self.i2c_read(self.i2c_buffer)
        return self.i2c_buffer[0] / 255

    @blacklight.setter
    def blacklight(self,val):
        self.i2c_buffer[0] = BLACKLIGHT | WRITE_MASK
        self.i2c_buffer[1] = int(255 * val)
        self.i2c_write(self.i2c_buffer)
    









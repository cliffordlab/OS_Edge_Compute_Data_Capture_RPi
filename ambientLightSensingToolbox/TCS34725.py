#!/usr/bin/python3
"""
Source: https://www.waveshare.com/w/upload/b/bb/TCS34725_Color_Sensor_user_manual_en.pdf
Please cite the manual as a reference if using this script.
Modified: Pradyumna Byappanahalli Suresha (alias Pradyumna94)
Last Modified: Mar 22nd, 2020

LICENSE:
This software is offered freely and without warranty under
the GNU GPL-3.0 public license. See license file for
more information
"""
import time
import math
import smbus
import pygame
import RPi.GPIO as GPIO


#GPIO 

LED     = 18
INT_PORT= 17

TCS34725_R_Coef     = 0.136 
TCS34725_G_Coef     = 1.000
TCS34725_B_Coef     = -0.444
TCS34725_GA         = 1.0
TCS34725_DF         = 310.0
TCS34725_CT_Coef    = 3810.0
TCS34725_CT_Offset  =1391.0

class TCS34725:
    Gain_t = 0
    IntegrationTime_t = 0

    TCS34725_CMD_BIT        = 0x80
    TCS34725_CMD_Read_Byte  = 0x00
    TCS34725_CMD_Read_Word  = 0x20
    TCS34725_CMD_Clear_INT  = 0x66 

    TCS34725_ENABLE         = 0x00
    TCS34725_ENABLE_AIEN    = 0x10    # RGBC Interrupt Enable  
    TCS34725_ENABLE_WEN     = 0x08     # Wait enable - Writing 1 activates the wait timer  
    TCS34725_ENABLE_AEN     = 0x02     # RGBC Enable - Writing 1 actives the ADC, 0 disables it  
    TCS34725_ENABLE_PON     = 0x01    # Power on - Writing 1 activates the internal oscillator, 0 disables it  
    TCS34725_ATIME          = 0x01    # Integration time  
    TCS34725_WTIME          = 0x03    # Wait time (if TCS34725_ENABLE_WEN is asserted)  
    TCS34725_WTIME_2_4MS    = 0xFF    # WLONG0 = 2.4ms   WLONG1 = 0.029s  
    TCS34725_WTIME_204MS    = 0xAB    # WLONG0 = 204ms   WLONG1 = 2.45s   
    TCS34725_WTIME_614MS    = 0x00    # WLONG0 = 614ms   WLONG1 = 7.4s    
    TCS34725_AILTL          = 0x04    # Clear channel lower interrupt threshold  
    TCS34725_AILTH          = 0x05
    TCS34725_AIHTL          = 0x06    # Clear channel upper interrupt threshold  
    TCS34725_AIHTH          = 0x07
    TCS34725_PERS           = 0x0C    # Persistence register - basic SW filtering mechanism for interrupts  
    TCS34725_PERS_NONE      = 0b0000  # Every RGBC cycle generates an interrupt                                 
    TCS34725_PERS_1_CYCLE   = 0b0001  # 1 clean channel value outside threshold range generates an interrupt    
    TCS34725_PERS_2_CYCLE   = 0b0010  # 2 clean channel values outside threshold range generates an interrupt   
    TCS34725_PERS_3_CYCLE   = 0b0011  # 3 clean channel values outside threshold range generates an interrupt   
    TCS34725_PERS_5_CYCLE   = 0b0100  # 5 clean channel values outside threshold range generates an interrupt   
    TCS34725_PERS_10_CYCLE  = 0b0101  # 10 clean channel values outside threshold range generates an interrupt  
    TCS34725_PERS_15_CYCLE  = 0b0110  # 15 clean channel values outside threshold range generates an interrupt  
    TCS34725_PERS_20_CYCLE  = 0b0111  # 20 clean channel values outside threshold range generates an interrupt  
    TCS34725_PERS_25_CYCLE  = 0b1000  # 25 clean channel values outside threshold range generates an interrupt  
    TCS34725_PERS_30_CYCLE  = 0b1001  # 30 clean channel values outside threshold range generates an interrupt  
    TCS34725_PERS_35_CYCLE  = 0b1010  # 35 clean channel values outside threshold range generates an interrupt  
    TCS34725_PERS_40_CYCLE  = 0b1011  # 40 clean channel values outside threshold range generates an interrupt  
    TCS34725_PERS_45_CYCLE  = 0b1100  # 45 clean channel values outside threshold range generates an interrupt  
    TCS34725_PERS_50_CYCLE  = 0b1101  # 50 clean channel values outside threshold range generates an interrupt  
    TCS34725_PERS_55_CYCLE  = 0b1110  # 55 clean channel values outside threshold range generates an interrupt  
    TCS34725_PERS_60_CYCLE  = 0b1111  # 60 clean channel values outside threshold range generates an interrupt  
    TCS34725_CONFIG         = 0x0D
    TCS34725_CONFIG_WLONG   = 0x02    # Choose between short and long (12x) wait times via TCS34725_WTIME  
    TCS34725_CONTROL        = 0x0F    # Set the gain level for the sensor  
    TCS34725_ID             = 0x12    # 0x44 = TCS34721/TCS34725, 0x4D = TCS34723/TCS34727  
    TCS34725_STATUS         = 0x13
    TCS34725_STATUS_AINT    = 0x10    # RGBC Clean channel interrupt  
    TCS34725_STATUS_AVALID  = 0x01    # Indicates that the RGBC channels have completed an integration cycle  
    TCS34725_CDATAL         = 0x14    # Clear channel data  
    TCS34725_CDATAH         = 0x15
    TCS34725_RDATAL         = 0x16    # Red channel data  
    TCS34725_RDATAH         = 0x17
    TCS34725_GDATAL         = 0x18    # Green channel data  
    TCS34725_GDATAH         = 0x19
    TCS34725_BDATAL         = 0x1A    # Blue channel data  
    TCS34725_BDATAH         = 0x1B
    
    #Integration Time
    TCS34725_INTEGRATIONTIME_2_4MS  = 0xFF   #<  2.4ms - 1 cycle    - Max Count: 1024
    TCS34725_INTEGRATIONTIME_24MS   = 0xF6   #<  24ms  - 10 cycles  - Max Count: 10240
    TCS34725_INTEGRATIONTIME_50MS   = 0xEB   #<  50ms  - 20 cycles  - Max Count: 20480 
    TCS34725_INTEGRATIONTIME_101MS  = 0xD5   #<  101ms - 42 cycles  - Max Count: 43008
    TCS34725_INTEGRATIONTIME_154MS  = 0xC0   #<  154ms - 64 cycles  - Max Count: 65535
    TCS34725_INTEGRATIONTIME_700MS  = 0x00   #<  700ms - 256 cycles - Max Count: 65535
    
    #Gain
    TCS34725_GAIN_1X                = 0x00   #<  No gain  */
    TCS34725_GAIN_4X                = 0x01   #<  4x gain  */
    TCS34725_GAIN_16X               = 0x02   #<  16x gain */
    TCS34725_GAIN_60X               = 0x03   #<  60x gain */
    
    R = 0
    G = 0
    B = 0
    C = 0
    
    RGB888_R = 0
    RGB888_G = 0
    RGB888_B = 0
    RGB888 = 0
    
    RGB565 = 0

    def __init__(self, address=0x29, debug=False):
        self.i2c = smbus.SMBus(1)
        self.address = address
        self.debug = debug
        #Set GPIO mode
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED, GPIO.OUT)
        self.pwm = GPIO.PWM(18, 1000)
        self.pwm.start(100)
        GPIO.setup(INT_PORT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        if (self.debug):
          print("Reseting TSL2581")

    def Write_Byte(self, reg, value):
        "Writes an 8-bit value to the specified register/address"
        reg = reg | self.TCS34725_CMD_BIT;#Register addressing highest bit is set to 1
        self.i2c.write_byte_data(self.address, reg, value)
        if (self.debug):
          print("I2C: Write 0x%02X to register 0x%02X" % (value, reg))
          
    def Write_Word(self, reg, value):
        "Writes an 8-bit value to the specified register/address"
        reg = reg | self.TCS34725_CMD_BIT;
        self.i2c.write_word_data(self.address, reg, value)
        if (self.debug):
          print("I2C: Write 0x%02X to register 0x%02X" % (value, reg))
          
    def Read_Byte(self, reg):
        "Read an unsigned byte from the I2C device"
        reg = reg | self.TCS34725_CMD_BIT;
        result = self.i2c.read_byte_data(self.address, reg)
        if (self.debug):
          print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, result & 0xFF, reg))
        return result
        
    def Read_Word(self, reg):
        "Read an unsigned byte from the I2C device"
        reg = reg | self.TCS34725_CMD_BIT;
        result = self.i2c.read_word_data(self.address, reg)
        if (self.debug):
          print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, result & 0xFF, reg))
        return result
        
    def Set_Gain(self, gain):
        self.Write_Byte(self.TCS34725_CONTROL, gain);
        self.Gain_t = gain;

    def Set_Integration_Time(self, time):
        # Update the timing register 
        self.Write_Byte(self.TCS34725_ATIME, time)
        self.IntegrationTime_t = time;

    def Enable(self):
        self.Write_Byte(self.TCS34725_ENABLE, self.TCS34725_ENABLE_PON)
        time.sleep(0.01)
        self.Write_Byte(self.TCS34725_ENABLE, self.TCS34725_ENABLE_PON | self.TCS34725_ENABLE_AEN)
        time.sleep(0.01) 

    def Disable(self):
        #Turn the device off to save power 
        reg = Read_Byte(self.TCS34725_ENABLE);
        self.Write_Byte(self.TCS34725_ENABLE, reg & ~(TCS34725_ENABLE_PON | TCS34725_ENABLE_AEN));
     
    def Interrupt_Enable(self):
        reg = self.Read_Byte(self.TCS34725_ENABLE)
        self.Write_Byte(self.TCS34725_ENABLE, reg | self.TCS34725_ENABLE_AIEN)

    def Interrupt_Disable(self):
        reg = self.Read_Byte(self.TCS34725_ENABLE)
        self.Write_Byte(self.TCS34725_ENABLE, reg & (~self.TCS34725_ENABLE_AIEN))

    def Set_Interrupt_Persistence_Reg(self, PER):
        if(PER < 0x10):
            self.Write_Byte(self.TCS34725_PERS, PER)
        else :
            self.Write_Byte(self.TCS34725_PERS, self.TCS34725_PERS_60_CYCLE)

    def Set_Interrupt_Threshold(self, Threshold_H,  Threshold_L):
        self.Write_Byte(self.TCS34725_AILTL, Threshold_L & 0xff)
        self.Write_Byte(self.TCS34725_AILTH, Threshold_L >> 8)
        self.Write_Byte(self.TCS34725_AIHTL, Threshold_H & 0xff)
        self.Write_Byte(self.TCS34725_AIHTH, Threshold_H >> 8)

    def Clear_Interrupt_Flag(self):
        self.Write_Byte(self.TCS34725_CMD_Clear_INT, 0x00);

    def TCS34725_init(self):
        ID = self.Read_Byte(self.TCS34725_ID)
        if(ID != 0x44 and ID != 0x4D):
            return 1
        self.Set_Integration_Time(self.TCS34725_INTEGRATIONTIME_154MS)
        self.Set_Gain(self.TCS34725_GAIN_60X)
        self.IntegrationTime_t = self.TCS34725_INTEGRATIONTIME_154MS
        self.Gain_t = self.TCS34725_GAIN_60X
        self.Enable()
        self.Interrupt_Enable()
        self.SetLight(40)
        return 0


    def GetLux_Interrupt(self, Threshold_H, Threshold_L):
        self.Set_Interrupt_Threshold(Threshold_H, Threshold_L);
        if(GPIO.input(INT_PORT) == GPIO.LOW):
            self.Clear_Interrupt_Flag();
            self.Set_Interrupt_Persistence_Reg(self.TCS34725_PERS_2_CYCLE);
            return 1;
        
        return 0;

    def Read_ID(self):
        return self.Read_Byte(self.TCS34725_ID)

    def Get_RGBData(self):
        self.C = self.Read_Word(self.TCS34725_CDATAL | self.TCS34725_CMD_Read_Word)
        self.R = self.Read_Word(self.TCS34725_RDATAL | self.TCS34725_CMD_Read_Word)
        self.G = self.Read_Word(self.TCS34725_GDATAL | self.TCS34725_CMD_Read_Word)
        self.B = self.Read_Word(self.TCS34725_BDATAL | self.TCS34725_CMD_Read_Word)
        if(self.IntegrationTime_t == self.TCS34725_INTEGRATIONTIME_2_4MS):
            time.sleep(0.01)
        elif(self.IntegrationTime_t == self.TCS34725_INTEGRATIONTIME_24MS):
            time.sleep(0.04)
        elif(self.IntegrationTime_t == self.TCS34725_INTEGRATIONTIME_50MS):
            time.sleep(0.05)
        elif(self.IntegrationTime_t == self.TCS34725_INTEGRATIONTIME_101MS):
            time.sleep(0.1)
        elif(self.IntegrationTime_t == self.TCS34725_INTEGRATIONTIME_154MS):
            time.sleep(0.2)
        elif(self.IntegrationTime_t == self.TCS34725_INTEGRATIONTIME_700MS):
            time.sleep(0.7)  

    #Convert read data to RGB888 format
    def GetRGB888(self):
        i = 1
        if(self.R >= self.G and self.R >= self.B): 
            i = self.R // 255 + 1
        
        elif( self.G >= self.R and self.G >= self.B):
            i =  self.G // 255 + 1

        elif(  self.B >=  self.G and self.B >= self.R):
            i =  self.B // 255 + 1 

        if(i!=0):
            self.RGB888_R = self.R // i
            self.RGB888_G = self.G // i
            self.RGB888_B = self.B // i

        if(self.RGB888_R > 30):
            self.RGB888_R = self.RGB888_R - 30
        if(self.RGB888_G > 30):
            self.RGB888_G = self.RGB888_G - 30
        if(self.RGB888_B > 30):
            self.RGB888_B = self.RGB888_B - 30
        
        self.RGB888_R = self.RGB888_R * 255 // 225
        self.RGB888_G = self.RGB888_G * 255 // 225
        self.RGB888_B = self.RGB888_B * 255 // 225
        
        self.RGB888 = (self.RGB888_R<<16) | (self.RGB888_G<<8) |(self.RGB888_B)

    def GetRGB565(self):
        i = 1
        RGB565_R = 0
        RGB565_G = 0
        RGB565_B = 0

        if(self.R >= self.G and self.R >= self.B): 
            i = self.R // 255 + 1
        elif( self.G >= self.R and self.G >= self.B):
            i =  self.G // 255 + 1
        elif(  self.B >=  self.G and self.B >= self.R):
            i =  self.B // 255 + 1 

        if(i!=0):
            RGB565_R = self.R // i
            RGB565_G = self.G // i
            RGB565_B = self.B // i

        if(RGB565_R > 30):
            RGB565_R = RGB565_R - 30
        if(RGB565_G > 30):
            RGB565_G = RGB565_G - 30
        if(RGB565_B > 30):
            RGB565_B = RGB565_B - 30
        
        RGB565_R = RGB565_R * 255 // 225
        RGB565_G = RGB565_G * 255 // 225
        RGB565_B = RGB565_B * 255 // 225  
        self.RG565 = (((RGB565_R>>3) << 11) | ((RGB565_G>>2) << 5) | (RGB565_B>>3 ))&0xffff

    def Get_Lux(self):
        
        atime_ms = ((256 - self.IntegrationTime_t) * 2.4);
        if(self.R + self.G + self.B > self.C):
            ir =  (self.R + self.G + self.B - self.C) // 2 
        else:
            ir = 0
            
        r_comp = self.R - ir;
        g_comp = self.G - ir;
        b_comp = self.B - ir;
        Gain_temp = 1
        if(self.Gain_t == self.TCS34725_GAIN_1X):
            Gain_temp = 1
        elif(self.Gain_t == self.TCS34725_GAIN_4X):
            Gain_temp = 4
        elif(self.Gain_t == self.TCS34725_GAIN_16X):
            Gain_temp = 16
        elif(self.Gain_t == self.TCS34725_GAIN_60X):
            Gain_temp = 60
 
        cpl = (atime_ms * Gain_temp) / (TCS34725_GA * TCS34725_DF);
        lux = (TCS34725_R_Coef * (float)(r_comp) + TCS34725_G_Coef * \
            (float)(g_comp) +  TCS34725_B_Coef * (float)(b_comp)) / cpl;
        return lux;

    def Get_Lux_noIRCompensation(self):
        
        atime_ms = ((256 - self.IntegrationTime_t) * 2.4);
            
        r_comp = self.R;
        g_comp = self.G;
        b_comp = self.B;
        Gain_temp = 1
        if(self.Gain_t == self.TCS34725_GAIN_1X):
            Gain_temp = 1
        elif(self.Gain_t == self.TCS34725_GAIN_4X):
            Gain_temp = 4
        elif(self.Gain_t == self.TCS34725_GAIN_16X):
            Gain_temp = 16
        elif(self.Gain_t == self.TCS34725_GAIN_60X):
            Gain_temp = 60
 
        cpl = (atime_ms * Gain_temp) / (TCS34725_GA * TCS34725_DF);
        lux = (TCS34725_R_Coef * (float)(r_comp) + TCS34725_G_Coef * \
            (float)(g_comp) +  TCS34725_B_Coef * (float)(b_comp)) / cpl;
        return lux;        
        

    def Get_ColorTemp(self):
        ir=1.0
        if(self.R + self.G + self.B > self.C):
            ir =  (self.R + self.G + self.B - self.C - 1) / 2 
        else:
            ir = 0
        r_comp = self.R - ir;
        b_comp = self.B - ir;
        cct=TCS34725_CT_Coef * (float)(b_comp) / (float)(r_comp) + TCS34725_CT_Offset;
        return cct;

    def SetLight(self, value):
        self.pwm.start(value)

        
        
        
        
        
        
        
        
        
        
        
        
        


\

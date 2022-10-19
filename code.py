from adafruit_debouncer import Debouncer
import digitalio
import board
import busio
import displayio
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import pwmio
import time
import gc

gc.enable()

# Counter for input weight to alarm at
counter = 0;

# Initializing all buttons and their pull up resistors.
button_input1 = digitalio.DigitalInOut(board.D10)
button_input2 = digitalio.DigitalInOut(board.D9)
button_input3 = digitalio.DigitalInOut(board.D8)
button_input4 = digitalio.DigitalInOut(board.D7)
button_input5 = digitalio.DigitalInOut(board.D6)

# Button.fell == True / Pushed
button_input1.switch_to_input(pull = digitalio.Pull.UP)
button_input2.switch_to_input(pull = digitalio.Pull.UP)
button_input3.switch_to_input(pull = digitalio.Pull.UP)
button_input4.switch_to_input(pull = digitalio.Pull.UP)
button_input5.switch_to_input(pull = digitalio.Pull.UP)

button1 = Debouncer(button_input1)
button2 = Debouncer(button_input2)
button3 = Debouncer(button_input3)
button4 = Debouncer(button_input4)
button5 = Debouncer(button_input5)

# Setting up pulse waves for buzzer
piezo = pwmio.PWMOut(board.D2, duty_cycle=0, frequency=440, variable_frequency=True)

# Setting up OLED
displayio.release_displays()
i2c = busio.I2C (scl=board.SCL, sda=board.SDA)

display_bus = displayio.I2CDisplay (i2c, device_address = 0x3C) # The address of my Board

oled = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
#Draw a smaller inner rectangle

current_counter = 0

font = terminalio.FONT

while True:
    #if (counter != current_counter):
    #    text = "Current Weight"
    #    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=28, y=15)
    #   splash.append(text_area)
    
    button1.update()
    button2.update()
    button3.update()
    button4.update()
    button5.update()
        
    if button1.fell:
        print("Button1 pressed")
        if (counter < 50):
            counter += 1

    if button1.rose:
        print("Button1 released")
        print(counter)
        
    
    if button2.fell:
        print("Button2 pressed")
        if (counter > 0):
            counter -= 1

    if button2.rose:
        print("Button2 released")
        print(counter)
        
    if button3.fell:
        print("Button3 pressed")

    if button3.rose:
        print("Button3 released")
    
    if button4.fell:
        print("Button4 pressed")

    if button4.rose:
        print("Button4 released")
        
    if button5.fell:
        print("Button5 pressed")

    if button5.rose:
        print("Button5 released")
   
        
    if (counter == 10):
        for f in (4500, 2700, 4500):
            piezo.frequency = f
            piezo.duty_cycle = 65535 // 2  # On 50%
            time.sleep(0.25)  # On for 1/4 second
            piezo.duty_cycle = 0  # Off
            time.sleep(0.05)  # Pause between notes
        counter -= 1
    
    text_display1 = "Current Weight\n"
    text_display2 = str(counter)

    #clock = label.Label(font, text=time_display)
    #date = label.Label(font, text=date_display)
    text1 = label.Label(font, text=text_display1)
    text2 = label.Label(font, text = text_display2)

    (_, _, width, _) = text1.bounding_box
    text1.x = oled.width // 2 - width // 2
    text1.y = 25
    
    (_, _, width, _) = text2.bounding_box
    text2.x = oled.width // 2 - width // 2
    text2.y = 35

    watch_group = displayio.Group()
    #watch_group.append(clock)
    #watch_group.append(date)
    watch_group.append(text1)
    watch_group.append(text2)

    oled.show(watch_group)
  
    
    #time.sleep(0.5)
    #gc.collect()
        



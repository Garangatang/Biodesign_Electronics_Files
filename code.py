from adafruit_debouncer import Debouncer
import digitalio
import board
import busio
import displayio
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label

# Counter for input weight to alarm at
counter = 0;

# Initializing all buttons and their pull up resistors.
button_input1 = digitalio.DigitalInOut(board.D0)
button_input2 = digitalio.DigitalInOut(board.D1)
button_input3 = digitalio.DigitalInOut(board.D2)
button_input4 = digitalio.DigitalInOut(board.D3)
button_input5 = digitalio.DigitalInOut(board.D7)

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

# Setting up OLED
displayio.release_displays()
i2c = busio.I2C (scl=board.SCL, sda=board.SDA)

display_bus = displayio.I2CDisplay (i2c, device_address = 0x3C) # The address of my Board

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
splash = displayio.Group() # no max_size needed
display.show(splash)

color_bitmap = displayio.Bitmap(128, 64, 1) # Full screen white
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White
 
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)
 
# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(118, 54, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=4)
splash.append(inner_sprite)

# Home screen
text = "Current Weight"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=28, y=15)
splash.append(text_area)

current_counter = 0

while True:
    if (counter != current_counter):
        text = "Current Weight"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=28, y=15)
        splash.append(text_area)
    
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
    
    if (counter != current_counter):
        # Blank slate
        #display.fill(1)
        #display.show()
        text1 = ""
        text_area1 = label.Label(terminalio.FONT, text=text1, color=0xFFFF00, x=32, y=25)
        splash.append(text_area1)
        # Show counter
        #text2 = "\t"+str(counter)
        #text_area2 = label.Label(terminalio.FONT, text=text2, color=0xFFFF00, x=32, y=25)
        #splash.append(text_area2)
        #current_counter = counter



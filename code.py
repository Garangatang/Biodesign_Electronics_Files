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
from cedargrove_nau7802 import NAU7802
from calibration import calibration

# String for setting screen mode


# set_weight for input weight to alarm at
set_weight = 6;
# Bool for sounding alarm or not
sound_alarm = True

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

# Button 1 is for increasing weight to alarm at
button1 = Debouncer(button_input1)
# Button 2 is for decreasing weight to alarm at
button2 = Debouncer(button_input2)
# Button 3 is for saving values to alarm at
button3 = Debouncer(button_input3)
# Button 4 is for switching screen modes
button4 = Debouncer(button_input4)
# Button 5 is for
button5 = Debouncer(button_input5)

# Setting up pulse waves for buzzer
piezo = pwmio.PWMOut(board.D2, duty_cycle=0, frequency=440, variable_frequency=True)

# Setting up OLED
displayio.release_displays()
i2c = busio.I2C (scl=board.SCL, sda=board.SDA)

display_bus = displayio.I2CDisplay (i2c, device_address = 0x3C) # The address of my Board

oled = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
#Draw a smaller inner rectangle

# Setting up i2c lines for load cell amplifier
nau7802 = NAU7802(i2c, address=0x2A, active_channels=2)
nau7802.gain = 128
enabled = nau7802.enable(True)

current_set_weight = 0
current_weight = 0;

font = terminalio.FONT

def zero_channel():
    """Initiate internal calibration for current channel; return raw zero
    offset value. Use when scale is started, a new channel is selected, or to
    adjust for measurement drift. Remove weight and tare from load cell before
    executing."""
    print(
        "channel %1d calibrate.INTERNAL: %5s"
        % (nau7802.channel, nau7802.calibrate("INTERNAL"))
    )
    print(
        "channel %1d calibrate.OFFSET:   %5s"
        % (nau7802.channel, nau7802.calibrate("OFFSET"))
    )
    zero_offset = read_raw_value(100)  # Read 100 samples to establish zero offset
    print("...channel %1d zeroed" % nau7802.channel)
    return zero_offset

def read_raw_value(samples=100):
    """Read and average consecutive raw sample values. Return average raw value."""
    sample_sum = 0
    sample_count = samples
    while sample_count > 0:
        if nau7802.available:
            sample_sum = sample_sum + nau7802.read()
            sample_count -= 1
    return int(sample_sum / samples)

#  function for finding the average of an array
def find_average(num):
    count = 0
    for n in num:
        count = count + n
    average = count / len(num)
    return average
#  calibration function

def calculateCalibration(array):
    for _ in range(10):
        nau7802.channel = 1
        #value = read_raw_value()
        print("channel %1.0f raw value: %7.0f" % (nau7802.channel, abs(read_raw_value())))
        array.append(abs(read_raw_value()))
        time.sleep(0.1)
    avg = find_average(array)
    return avg

#print("*** Instantiate and calibrate load cells")
text_display1 = "*** Instantiate and \ncalibrate load cells"

text1 = label.Label(font, text = text_display1)

(_, _, width, _) = text1.bounding_box
text1.x = oled.width // 2 - width // 2
text1.y = 25

screen_group = displayio.Group()

screen_group.append(text1)

oled.show(screen_group)


# Instantiate and calibrate load cell inputs

# Enable NAU7802 digital and analog power
enabled = nau7802.enable(True)
print("Digital and analog power enabled:", enabled)
text_display1 = "Digital and analog\n power enabled:"

text1 = label.Label(font, text = text_display1)

(_, _, width, _) = text1.bounding_box
text1.x = oled.width // 2 - width // 2
text1.y = 25

screen_group = displayio.Group()

screen_group.append(text1)


oled.show(screen_group)


print("REMOVE WEIGHTS FROM LOAD CELLS")
text_display1 = "REMOVE WEIGHTS\n FROM LOAD CELL"

text1 = label.Label(font, text = text_display1)

(_, _, width, _) = text1.bounding_box
text1.x = oled.width // 2 - width // 2
text1.y = 25

screen_group = displayio.Group()

screen_group.append(text1)

oled.show(screen_group)

time.sleep(2)

# Zero out the channels
#  runs the calculateCallibration function
#  takes 10 raw readings, stores them into an array and gets an average
zero_readings = []
zero_avg = calculateCalibration(zero_readings)
# Calibrating the channels
nau7802.channel = 1
zero_channel()  # Calibrate and zero channel
nau7802.channel = 2
zero_channel()  # Calibrate and zero channel
weight_readings = []
#  weighs the item 10 times, stores the readings in an array & averages them
weight_avg = calculateCalibration(weight_readings)
#  calculates the new offset value
calibration['offset_val'] = (weight_avg-zero_avg) / calibration['weight']

print("READY")
text_display1 = "Place IV\nBag On Hook"

text1 = label.Label(font, text = text_display1)

(_, _, width, _) = text1.bounding_box
text1.x = oled.width // 2 - width // 2
text1.y = 25

screen_group = displayio.Group()

screen_group.append(text1)

oled.show(screen_group)
time.sleep(1)

# Initializing calibration values for the load cell
stage = 0
zero_stage = 0
weight_avg = 0
zero_avg = 0
show_oz = True
show_grams = False
zero_out = False
calibrate_mode = False
blue_btn_pressed = False
green_btn_pressed = False
run_mode = True
avg_read = []
values = []
val_offset = 0
avg_values = []
screenMode = "raw"

for w in range(5):
    nau7802.channel = 1
    value = read_raw_value()
    #  takes value reading and divides with by the offset value
    #  to get the weight in grams
    grams = value / calibration['offset_val']
    avg_read.append(grams)
    if len(avg_read) > 4:
        the_avg = find_average(avg_read)
        oz = the_avg / 28.35
        #display.print("   %0.1f oz" % oz)
        avg_read.clear()
    time.sleep(0.5)

while True:
    
    button1.update()
    button2.update()
    button3.update()
    button4.update()
    button5.update()
        
    if button1.fell:
        print("Button1 pressed")
        if (screenMode == "setWeight"):
            set_weight += 1

    if button1.rose:
        print("Button1 released")
        print(set_weight)
        
    # Decrease weight to alarm at
    if button2.fell:
        print("Button2 pressed")
        if (set_weight > 6 and screenMode == "setWeight"):
            set_weight -= 1

    if button2.rose:
        print("Button2 released")
        print(set_weight)
    
    # Return to showing the raw loading values
    if button3.fell:
        screenMode = "raw"
        print("Button3 pressed")

    if button3.rose:
        print("Button3 released")
    
    # Button to change the screen modes to set the weight to alarm at
    if button4.fell:
        screenMode = "setWeight"
        print("Button4 pressed")

    if button4.rose:
        print("Button4 released")
    
    # Set button to turn alarm on and off
    if button5.fell:
        sound_alarm = not sound_alarm
        #pr
        print("Button5 pressed")

    if button5.rose:
        print("Button5 released")
   
    # Setting off the buzzer if set_weight hits a set value
    if (current_weight <= set_weight*5 and sound_alarm):
        for f in (3600, 2700, 3600):
            piezo.frequency = f
            piezo.duty_cycle = 65535 // 2  # On 50%
            time.sleep(0.25)  # On for 1/4 second
            piezo.duty_cycle = 0  # Off
            time.sleep(0.05)  # Pause between notes
        #set_weight -= 1
    
    if (screenMode == "raw"):

        nau7802.channel = 1
        value = read_raw_value()
        #print(value)
        value = abs(value) - val_offset
        #print(value)
        #value = abs(value)
        values.append(value)
        #  takes value reading and divides with by the offset value
        #  to get the weight in grams
        grams = value / calibration['offset_val']
        current_weight = grams* -11.0
        
        #oz = grams / 28.35
        
        avg_read.append(current_weight)
        #label1 = "g"
        print(avg_read)
        # Averaging all the reads so a sudden spike doesn't skew the readings too much
        if (len(avg_read) > 10):
            the_avg = find_average(avg_read)
            #display.print("   %0.1f %s" % (the_avg, label))
            avg_read.clear()
        
        text_display4 = "Current Weight"
        text_display2 = "Set Weight: " + str(set_weight*5)
        #nau7802.channel = 1
        #value = read_raw_value()
        text_display3 = "raw value in g: %3.1f" % (current_weight)

        text4 = label.Label(font, text = text_display4)
        text2 = label.Label(font, text = text_display2)
        text3 = label.Label(font, text = text_display3)

        (_, _, width, _) = text4.bounding_box
        text4.x = oled.width // 2 - width // 2
        text4.y = 25
        
        (_, _, width, _) = text2.bounding_box
        text2.x = oled.width // 2 - width // 2
        text2.y = 35
        
        (_, _, width, _) = text3.bounding_box
        text3.x = oled.width // 2 - width // 2
        text3.y = 45

        screen_group = displayio.Group()

        screen_group.append(text4)
        screen_group.append(text2)
        screen_group.append(text3)
        
        # Showing an updating screen group with the current weight and set weight
        oled.show(screen_group)
    
    # Change the screen to allow users to change the weight
    if (screenMode == "setWeight"):
        text_display1 = "Weight to Alarm At"
        text_display2 = "Set Weight: %4.0f" % (set_weight * 5)
        alarm_status = "off"
        if (sound_alarm):
            alarm_status = "on"
            
        text_display3 = "Alarm status: " + alarm_status

        text1 = label.Label(font, text = text_display1)
        text2 = label.Label(font, text = text_display2)
        text3 = label.Label(font, text = text_display3)

        (_, _, width, _) = text1.bounding_box
        text1.x = oled.width // 2 - width // 2
        text1.y = 25
        
        (_, _, width, _) = text2.bounding_box
        text2.x = oled.width // 2 - width // 2
        text2.y = 35
        
        (_, _, width, _) = text3.bounding_box
        text3.x = oled.width // 2 - width // 2
        text3.y = 45

        screen_group = displayio.Group()

        screen_group.append(text1)
        screen_group.append(text2)
        screen_group.append(text3)
        
        oled.show(screen_group)
        #sound_alarm = True
    #print(screenMode)



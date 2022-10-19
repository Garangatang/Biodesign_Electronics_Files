import time
import displayio
import terminalio
import busio
import board
import adafruit_displayio_ssd1306
import adafruit_pcf8563
from cedargrove_nau7802 import NAU7802

from adafruit_display_text import label

displayio.release_displays()

i2c = busio.I2C(scl=board.SCL, sda=board.SDA)

#nau7802 = NAU7802(i2c, address=0x2A, active_channels=2)
pcf8563 = adafruit_pcf8563.PCF8563(i2c)

font = terminalio.FONT

display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)  # The address of my Board
rtc = adafruit_pcf8563.PCF8563(i2c)

oled = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

while True:
    current = pcf8563.datetime
            
    # Formatting current time according to ISO 8601 
    #current_time = datetime(*current[:6]).isoformat()
    #current = rtc.datetime

    hour = current.tm_hour % 12
    if hour == 0:
        hour = 12

    am_pm = "AM"
    if current.tm_hour / 12 >= 1:
        am_pm = "PM"

    time_display = "{:d}:{:02d}:{:02d} {}".format(hour, current.tm_min, current.tm_sec, am_pm)
    date_display = "{:d}/{:d}/{:d}".format(current.tm_mon, current.tm_mday, current.tm_year)
    text_display = "CircuitPython Time"

    clock = label.Label(font, text=time_display)
    date = label.Label(font, text=date_display)
    text = label.Label(font, text=text_display)

    (_, _, width, _) = clock.bounding_box
    clock.x = oled.width // 2 - width // 2
    clock.y = 5

    (_, _, width, _) = date.bounding_box
    date.x = oled.width // 2 - width // 2
    date.y = 15

    (_, _, width, _) = text.bounding_box
    text.x = oled.width // 2 - width // 2
    text.y = 25

    watch_group = displayio.Group()
    watch_group.append(clock)
    watch_group.append(date)
    watch_group.append(text)

    oled.show(watch_group)


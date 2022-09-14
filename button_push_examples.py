from adafruit_debouncer import Debouncer
import digitalio
import board

button_input1 = digitalio.DigitalInOut(board.D0)
button_input2 = digitalio.DigitalInOut(board.D2)
button_input3 = digitalio.DigitalInOut(board.D3)
button_input4 = digitalio.DigitalInOut(board.D4)
button_input5 = digitalio.DigitalInOut(board.D5)

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

while True:
    button1.update()
    button2.update()
    button3.update()
    button4.update()
    button5.update()

    if button1.fell:
        print("Button1 pressed")

    if button1.rose:
        print("Button1 released")
    
    if button2.fell:
        print("Button2 pressed")

    if button2.rose:
        print("Button2 released")
        
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

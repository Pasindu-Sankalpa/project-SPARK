import RPi.GPIO as IO

pwm_pins = [12, 13, 18, 19]

def set_GPIO():
    lines = []
    IO.setwarnings(False)
    IO.cleanup()
    IO.setmode(IO.BCM)

    for pin in pwm_pins:
        IO.setup(pin, IO.OUT)
        output = IO.PWM(pin, 100)
        output.start(0)
        lines.append(output)

    return lines

def controller(line, duty, stop):
    if duty > 4: duty = 4
    duty *= 25
    print("PWM Duty = ", duty, "%")
    line.ChangeDutyCycle(duty)

    while True:
        if stop(): 
            break
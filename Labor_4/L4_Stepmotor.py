"""-----------------------------------------------------
¦    File name: L4_Stepmotor.py                         ¦
¦    Version: 1.2                                       ¦
¦    Authors:                                           ¦
¦       Jonas Josi                                      ¦
¦       Matthias Lang                                   ¦
¦       Christian Hohmann                               ¦
¦       Joschka Maters                                  ¦
¦    Date created: 2024/05/01                           ¦
¦    Last modified: 2025/01/20                          ¦
¦    Python Version: 3.11.2                             ¦
------------------------------------------------------"""

# ----------- import external Python module -----------
import lgpio
import time


# ----------- global constant -----------
# assign motor driver interface to GPIO's of Raspberry Pi (DRV8825)
DIR = 17    # Direction
STEP = 18   # Step pulse
SLP = 27    # Sleep (active HIGH to enable)
RST = 22    # Reset (active HIGH to enable)

# settings of stepper motor
DIRECTION = 0  # *** CHANGE ME *** movement direction (0 or 1) of slide on linear guideway
STEP_TIME = 0.003  # *** CHANGE ME *** time in [s] between two consecutive steps of stepper motor

# ----------- function definition -----------
def set_motor_coils(direction, step_state):
    """
    Set direction (DIR pin) and pulse the STEP pin of the DRV8825 motor driver.
    Parameters
    ----------
    direction : int or GPIO.LOW or GPIO.HIGH
        Direction of rotation (0 or 1), written to the DIR pin.
    step_state : int or GPIO.LOW or GPIO.HIGH
        State of the STEP pin (0 or 1). Toggling this HIGH then LOW advances the motor one step.
    """
    lgpio.gpio_write(gpio0, DIR, direction)
    lgpio.gpio_write(gpio0, STEP, step_state)


def busy_sleep(secs):
    """
    Actively waits for a specified time by keeping the CPU busy in a loop. This has the advantage over a passive sleep
    (i.e. time.sleep()) that a more precise timing / sleep time can be achieved. However, it may consume more
    CPU resources compared to a passive sleep method.

    Parameters
    ----------
    secs : float
        The wait time in seconds. Can be a decimal number.
    """
    start_timestamp = time.time()
    # if sleep time is more than 4 ms, make a passive sleep of sleep time - 2 ms to reduce cpu resources
    if secs > 0.0004:
        time.sleep(secs - 0.0002)
    while time.time() - start_timestamp < secs:
        pass  # do nothing


def stop_motor():
    """
    Set STEP pin LOW and put the DRV8825 driver to sleep (SLP LOW) to de-energize the motor coils.
    """

    # stop stepping and disable driver outputs
    lgpio.gpio_write(gpio0, STEP, 0)
    lgpio.gpio_write(gpio0, SLP, 0)
    busy_sleep(STEP_TIME)

    print("\nMotor stopped")


# ----------- main code -----------
if __name__ == "__main__":
    # initialize lgpio
    gpio0 = lgpio.gpiochip_open(0) # open GPIO chip 0

    # Configure GPIO pins as outputs
    lgpio.gpio_claim_output(gpio0, DIR)
    lgpio.gpio_claim_output(gpio0, STEP)
    lgpio.gpio_claim_output(gpio0, SLP)
    lgpio.gpio_claim_output(gpio0, RST)

    # initialize all pins to safe state
    lgpio.gpio_write(gpio0, DIR, 0)
    lgpio.gpio_write(gpio0, STEP, 0)
    lgpio.gpio_write(gpio0, RST, 1)  # RST HIGH = not reset
    lgpio.gpio_write(gpio0, SLP, 1)  # SLP HIGH = not sleeping (driver enabled)
    time.sleep(0.001)

    try:
        # endless loop
        while True:
            # pulse STEP pin HIGH then LOW in the configured DIRECTION to advance one step
            set_motor_coils(DIRECTION, 1)
            busy_sleep(STEP_TIME)
            set_motor_coils(DIRECTION, 0)
            busy_sleep(STEP_TIME)

    # detect exception - usually triggered by a user input, stopping the script
    except KeyboardInterrupt:
        stop_motor()
        # Free GPIO pins
        lgpio.gpio_free(gpio0, DIR)
        lgpio.gpio_free(gpio0, STEP)
        lgpio.gpio_free(gpio0, SLP)
        lgpio.gpio_free(gpio0, RST)
        lgpio.gpiochip_close(gpio0) # Close the GPIO chip connection
        print("Exit Python")
        exit(0)  # exit python with exit code 0
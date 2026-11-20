"""-----------------------------------------------------
¦    File name: L4_Stepmotor_Measurements.py            s¦
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


# settings of stepper motor and cycles/movement
STEP_TIME = 0.0005  # *** CHANGE ME *** time in [s] between two consecutive steps of stepper motor
MOVEMENT_STOP_TIME = 3  # *** CHANGE ME ***  Pause [s] between two consecutive movements (up/down) of slide on linear guideway
MOVEMENT_STEP_NUMBER = 2000  # *** CHANGE ME ***  Number of steps to drive the stepper motor per movement of the slide on the linear guideway
CYCLE_START_DIRECTION = 1  # *** CHANGE ME ***  Direction (0 or 1) of first movement of slide on linear guideway
CYCLE_NUMBER = 3  # *** CHANGE ME ***  Number of cycles (movement of slide on linear guideway in one direction, followed by movement in the opposite direction)


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
    lgpio.gpio_write(gpio0, DIR,  direction)
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
        time.sleep(secs - secs / 10)
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

    # initialize all pins to safe stat
    lgpio.gpio_write(gpio0, DIR, 0)
    lgpio.gpio_write(gpio0, STEP, 0)
    lgpio.gpio_write(gpio0, RST, 1)  # RST HIGH = not reset
    lgpio.gpio_write(gpio0, SLP, 1)  # SLP HIGH = not sleeping (driver enabled)
    time.sleep(0.001)


    """ start measurement """
    try:
        direction = CYCLE_START_DIRECTION
        step = 0
        cycle = 0
        # endless loop
        while cycle < CYCLE_NUMBER:
            if direction == 0:
                while step < MOVEMENT_STEP_NUMBER:
                    # pulse STEP pin (1st step of this pass)
                    set_motor_coils(direction, 1)
                    busy_sleep(STEP_TIME)
                    set_motor_coils(direction, 0)
                    busy_sleep(STEP_TIME)

                    step += 1

                    if step >= MOVEMENT_STEP_NUMBER:
                        break  # leave while-loop
                    # pulse STEP pin (2nd step of this pass)
                    set_motor_coils(direction, 1)
                    busy_sleep(STEP_TIME)
                    set_motor_coils(direction, 0)
                    busy_sleep(STEP_TIME)
                    step += 1

                    if step >= MOVEMENT_STEP_NUMBER:
                        break  # leave while-loop
                    # pulse STEP pin (3rd step of this pass)
                    set_motor_coils(direction, 1)
                    busy_sleep(STEP_TIME)
                    set_motor_coils(direction, 0)
                    busy_sleep(STEP_TIME)
                    step += 1

                    if step >= MOVEMENT_STEP_NUMBER:
                        break  # leave while-loop
                    # pulse STEP pin (4th step of this pass)
                    set_motor_coils(direction, 1)
                    busy_sleep(STEP_TIME)
                    set_motor_coils(direction, 0)
                    busy_sleep(STEP_TIME)
                    step += 1

                    if step >= MOVEMENT_STEP_NUMBER:
                        break  # leave while-loop
            elif direction == 1:
                while step < MOVEMENT_STEP_NUMBER:
                    # pulse STEP pin (1st step of this pass)
                    set_motor_coils(direction, 1)
                    busy_sleep(STEP_TIME)
                    set_motor_coils(direction, 0)
                    busy_sleep(STEP_TIME)
                    step += 1

                    if step >= MOVEMENT_STEP_NUMBER:
                        break  # leave while-loop
                    # pulse STEP pin (2nd step of this pass)
                    set_motor_coils(direction, 1)
                    busy_sleep(STEP_TIME)
                    set_motor_coils(direction, 0)
                    busy_sleep(STEP_TIME)
                    step += 1

                    if step >= MOVEMENT_STEP_NUMBER:
                        break  # leave while-loop
                    # pulse STEP pin (3rd step of this pass)
                    set_motor_coils(direction, 1)
                    busy_sleep(STEP_TIME)
                    set_motor_coils(direction, 0)
                    busy_sleep(STEP_TIME)
                    step += 1

                    if step >= MOVEMENT_STEP_NUMBER:
                        break  # leave while-loop
                    # pulse STEP pin (4th step of this pass)
                    set_motor_coils(direction, 1)
                    busy_sleep(STEP_TIME)
                    set_motor_coils(direction, 0)
                    busy_sleep(STEP_TIME)
                    step += 1

            step = 0
            direction = not direction  # change direction
            cycle += 0.5

            # check if last movement of measurement is not already done
            if cycle != CYCLE_NUMBER:
                # wait between movements
                time.sleep(MOVEMENT_STOP_TIME)

        stop_motor()
        # Free GPIO pins
        lgpio.gpio_free(gpio0, DIR)
        lgpio.gpio_free(gpio0, STEP)
        lgpio.gpio_free(gpio0, SLP)
        lgpio.gpio_free(gpio0, RST) # Close the GPIO chip connection
        print("Exit Python")
        exit(0)  # exit python with exit code 0

    # detect exception - usually triggered by a user input, stopping the script
    except KeyboardInterrupt:
        stop_motor()
        # Free GPIO pins
        lgpio.gpio_free(gpio0, DIR)
        lgpio.gpio_free(gpio0, STEP)
        lgpio.gpio_free(gpio0, SLP)
        lgpio.gpio_free(gpio0, RST)  # Close the GPIO chip connection
        print("Exit Python")
        exit(0)  # exit python with exit code 0
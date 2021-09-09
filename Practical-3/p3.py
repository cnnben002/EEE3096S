# Import libraries
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os
import math
import time

# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game
pwmLed = None       # set a pwm variable for the led
pwmBuzzer = None    # set a pwm variable for the buzzer
rand_value = 0      # random value that user has to guess
user_guess = 1      # user number guess
score_count = 4
attempts = 0

# DEFINE THE PINS USED HERE
LED_value = [11, 13, 15]
LED_accuracy = 32
btn_submit = 16
btn_increase = 18
buzzer = 33
eeprom = ES2EEPROMUtils.ES2EEPROM()


# Print the game banner
def welcome():
    os.system('clear')
    print("  _   _                 _                  _____ _            __  __ _")
    print("| \ | |               | |                / ____| |          / _|/ _| |")
    print("|  \| |_   _ _ __ ___ | |__   ___ _ __  | (___ | |__  _   _| |_| |_| | ___ ")
    print("| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  \___ \| '_ \| | | |  _|  _| |/ _ \\")
    print("| |\  | |_| | | | | | | |_) |  __/ |     ____) | | | | |_| | | | | | |  __/")
    print("|_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_____/|_| |_|\__,_|_| |_| |_|\___|")
    print("")
    print("Guess the number and immortalise your name in the High Score Hall of Fame!")


# Print the game menu
def menu():
    global end_of_game
    global rand_value
    global attempts
    global user_guess
    global pwmLed
    global pwmBuzzer
    option = input("Select an option:   H - View High Scores     P - Play Game       Q - Quit\n")
    option = option.upper()
    if option == "H":
        os.system('clear')
        print("HIGH SCORES!!")
        s_count, ss = fetch_scores()
        display_scores(s_count, ss)
    elif option == "P":
        os.system('clear')
        print("Starting a new round!")
        print("Use the buttons on the Pi to make and submit your guess!")
        print("Press and hold the guess button to cancel your game")
        rand_value = generate_number()
        end_of_game = False
        attempts = 0
        user_guess = 1
        pwmLed.start(0)
        pwmBuzzer.start(0)
        display_led_num(user_guess)
        while not end_of_game:
            pass
    elif option == "Q":
        print("Come back soon!")
        exit()
    else:
        print("Invalid option. Please select a valid one!")


def display_scores(count, raw_data):
    # print the scores to the screen in the expected format
    print("There are {} scores. Here are the top 3!".format(count))
    # print out the scores in the required format
    raw_data.sort()
    name = raw_data[0]
    print("1 - {} took {} guesses".format(name[1:], name[:1]))
    name = raw_data[1]
    print("2 - {} took {} guesses".format(name[1:], name[:1]))
    name = raw_data[2]
    print("3 - {} took {} guesses".format(name[1:], name[:1]))
    pass


# Setup Pins
def setup():
    # Setup board mode
    GPIO.setmode(GPIO.BOARD)

   # Setup regular GPIO
    GPIO.setup(LED_value, GPIO.OUT)
    GPIO.setup(LED_accuracy, GPIO.OUT)
    GPIO.setup(buzzer, GPIO.OUT)
    GPIO.setup(btn_submit, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_increase, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Setup PWM channels
    global pwmLed
    global pwmBuzzer
    pwmLed = GPIO.PWM(LED_accuracy, 1000)
    pwmLed.start(0)
    pwmBuzzer = GPIO.PWM(buzzer, 10)
    pwmBuzzer.start(0)

    # Setup debouncing and callbacks
    GPIO.add_event_detect(btn_submit, edge=GPIO.RISING, callback=btn_guess_pressed, bouncetime=200)
    GPIO.add_event_detect(btn_increase, edge=GPIO.RISING, callback=btn_increase_pressed, bouncetime=200)
    pass


# Load high scores
def fetch_scores():
    # get however many scores there are
    global score_count
    scores = []
    endByte = score_count*4+4

    # Get the scores
    ascores = eeprom.read_block(0, endByte)

    # convert the codes back to ascii
    for i in range(4, endByte-1, 4):
        name = str(ascores[i+3])
        for j in range(3):
            name += chr(ascores[i+j])
        scores.append(name)

    # return back the results
    return score_count, scores


# Save high scores
def save_scores(newScore):
    # fetch scores
    global score_count
    s_count, ss = fetch_scores()

    # include new score
    if(newScore != ""):
        ss.append(newScore)

    # sort
    ss.sort()

    # update total amount of scores
    score_count = len(ss)

    # write new score
    startbyte = score_count * 4

    for i in range(3):
        eeprom.write_byte(startbyte+i, ord(newScore[i]))
    eeprom.write_byte(startbyte+3, int(newScore[3]))
    pass


# Generate guess number
def generate_number():
    return random.randint(1, pow(2, 3)-1)

# Display numbers via LEDs
def display_led_num(value):
    val1 = 0
    val2 = 0
    val3 = 0

    if(value%2 != 0):
        val1 = value%2;

    value = math.floor(value/2)

    if(value%2 != 0):
        val2 = value%2;

    value = math.floor(value/2)

    if(value%2 != 0):
        val3 = value%2;

    value = math.floor(value/2)

    if(val1 == 1):
    	GPIO.output(LED_value[0], GPIO.HIGH)
    else:
    	GPIO.output(LED_value[0], GPIO.LOW)

    if(val2 == 1):
        GPIO.output(LED_value[1], GPIO.HIGH)
    else:
        GPIO.output(LED_value[1], GPIO.LOW)

    if(val3 == 1):
        GPIO.output(LED_value[2], GPIO.HIGH)
    else:
        GPIO.output(LED_value[2], GPIO.LOW)
    pass

# Increase button pressed
def btn_increase_pressed(channel):
    global user_guess
    user_guess += 1

    if(user_guess == 8):
        user_guess -= 7

    display_led_num(user_guess)
    pass


# Guess button
def btn_guess_pressed(channel):
    # If they've pressed and held the button, clear up the GPIO and take them back to the menu screen
    global end_of_game
    global pwmLed
    global pwmBuzzer
    global buzzer

    start_time = time.time()
    pushTime = 0

    while (GPIO.input(channel) == GPIO.LOW):
        pushTime = time.time() - start_time

        if(pushTime >= 2.5):
            break

        pass

    if(pushTime >= 2.3):
        end_of_game = True

    # Compare the actual value with the user value displayed on the LEDs
    global rand_value
    global user_guess
    global attempts

    attempts += 1
    percent = float(user_guess)/rand_value*100

    if(percent > 100):
        percent = float(rand_value)/user_guess*100

    accuracy_leds(percent)
    trigger_buzzer()

    # if it's an exact guess:
    # - Disable LEDs and Buzzer
    if(rand_value == user_guess and end_of_game == False):
        GPIO.output(LED_value, GPIO.LOW)
        pwmLed.stop()
        pwmBuzzer.stop()

        # - tell the user and prompt them for a name
        print("Well Done - Correct Guess!!")
        name = input("Please enter your  name: \n")

        while(len(name) != 3):
            print("Name must be 3 letters long - try again")
            name = input("Please enter your name: \n")

    	# - add the new score
        newScore = name + str(attempts)
        save_scores(newScore)

        end_of_game = True

    if(end_of_game == True):
        GPIO.output(LED_value, GPIO.LOW)
        pwmLed.stop()
        pwmBuzzer.stop()
    pass


# LED Brightness
def accuracy_leds(percent):
    pwmLed.ChangeDutyCycle(percent)
    pass

# Sound Buzzer
def trigger_buzzer():
    global  user_guess
    global rand_value
    diff = abs(user_guess  - rand_value)

    if(diff == 3):
        pwmBuzzer.start(50)
        pwmBuzzer.ChangeFrequency(1)
    elif(diff == 2):
        pwmBuzzer.start(50)
        pwmBuzzer.ChangeFrequency(2)
    elif(diff == 1):
        pwmBuzzer.start(50)
        pwmBuzzer.ChangeFrequency(4)
    else:
        pwmBuzzer.stop()
    pass

# Main
if __name__ == "__main__":
    try:
        setup()
        welcome()
        eeprom.populate_mock_scores()
        while True:
            menu()
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()

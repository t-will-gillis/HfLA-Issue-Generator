from time import sleep   


def countdown(secs):
    """
    Countdown timer 
    """
    i = 0
    while secs > 0:

        # Prints the timer
        print('HOLDING' + '.' * i, end='\r')
        
        # Delays the program and decrements by quarter second
        sleep(.25)
        secs -= .25
        i += 1

    print('HOLDING' + '.' * i +'Ready!')
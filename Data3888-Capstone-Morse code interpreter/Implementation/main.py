import os
import argparse
from UI import UserInterface
from catch_for_main_loop import streaming_classifier

## the main loop
# /Users/oliveroayda/Desktop/Code/blinking
##the loop that updates every time something happens

def flag_setup():
    ''' Handles flags for the main program program'''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--static', '-s', help='tells the main loop it is not handling live input, instead it is handling a static array, For debugging.',action='store_true')
    parser.add_argument('--line', '-l', help='tells the main loop it is not handling spikerbox input, instead it is handling commandline input, For debugging.',action='store_true')
    parser.add_argument('--simulate', '-x', help='tells the main loop it is handling a simulated spikerbox input',action='store_true')
    parser.add_argument('--actual', '-a', help='The epic main loop.',action='store_true')
    return parser.parse_args()

def streamingIn(application):
    ''' handles streaming input'''
    print('stream')

def staticIn(A,application):
    ''' handles static array input'''
    print('static')

def lineIn(application):
    '''handles commandline input'''
    while application.open:
        bidding = input('what is your bidding?')
        if bidding in ['-1','0','1','2','-2']:
            application.inputNumber(int(bidding))
            application.update()
        else:
            print("sorry I dont understand your bidding, try 1, 0 or -1")

def main():
    #while propgram runs, execute loop
    print("Main loop initiated.")
    flags = flag_setup()
    userInt = UserInterface()

if __name__ == "__main__":
    main()
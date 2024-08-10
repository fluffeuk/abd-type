import curses
from curses import wrapper

import random
import time

# function to start the timer 
def time_start(): return time.time()

# sentence generation (list must be in this file's directory)
def sentencegen(list, n):
    with open(list, 'r') as file:
        words = file.read().split()
    
    return ' '.join(random.sample(words, n)) + '.'

# check if typed character is correct
def comparech(pressed_key, correct_key_index, s):
    correct_key = s[correct_key_index]
    return pressed_key == correct_key

# WPM checker(burst, refreshes for every word typed, or every element in the user input list)
def burstwpm(stdscr, user_input, start_time):
    time_elapsed = time.time() - start_time
    if time_elapsed > 0 and len(user_input) > 0:
        stdscr.addstr(2, 0, f"{(len(user_input)/(time_elapsed) * 60):.2f}WPM")
        #without the 60 its words per second. you want to times it by 60 to get a minute
        
    
# displaying in terminal
def main(stdscr):   
    stdscr.clear()
    stdscr.refresh()
    
    random_sentence = sentencegen("1000-most-common-words.txt", 15)
    user_input = []
    
    stdscr.addstr(0, 0, random_sentence, curses.A_DIM)
    keypress_count = 0
    last_word_count = 0
    
    stdscr.move(0, 0)
    
    while keypress_count < len(random_sentence):
        key = stdscr.getkey()
        
        # store the time at which the user started typing
        if not user_input:
            start_time = time_start()
            
        if key == "\x7f":
            if keypress_count > 0:
                keypress_count -= 1
                user_input.pop() #removes last element in the list
                stdscr.clear()
                stdscr.addstr(0, 0, random_sentence, curses.A_DIM)
                stdscr.addstr(0, 0, ''.join(user_input))
                
        elif comparech(key, keypress_count, random_sentence):
            stdscr.addstr(0, keypress_count, key)
            user_input.append(key)
            keypress_count += 1
            
        stdscr.refresh()
        
wrapper(main)

# CURSES-INFO

#curses uses buffers to make changes to the terminal more efficiently. this way, it can perform several changes without them 
# being immediately visible, and once all the changes needed are done, it only needs to update once for all of the changes to 
# take effect, this is what stdscr.refresh() does.

#The buffer is a temporary storage space where changes to the display are accumulated. once all of the changes are done stacking, 
# a single refresh will deliver all the changes to the screen.
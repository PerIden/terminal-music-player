import pygame
from pygame import mixer
import os
from os import listdir
import curses
from math import *

def print_menu(stdscr, selected_row_idx):
    height, width = stdscr.getmaxyx()

    stdscr.border(0)

    box_menu = curses.newwin(height,width,0,0)
    box_menu.box()
    
    stdscr.clear()
    menu = os.listdir()
    stdscr.refresh()
    box_menu.refresh()
    for idx, row in enumerate(menu):
        x = width//2 - len(row)//2
        y = height//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            try:
                stdscr.addstr(y, x, row)
            except curses.error:
                pass
            stdscr.attroff(curses.color_pair(1))
        else:
            try:
                stdscr.addstr(y, x, row)
            except curses.error:
                pass
        
    stdscr.refresh()

def navigation(current_row, stdscr):
    while 1:
        try:
            curses.curs_set(0)
        except:
            pass
        key = stdscr.getch()
        menu = os.listdir()
        #stdscr.refresh()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu)-1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]: 
           if os.path.isdir(menu[current_row]) == True:
                os.chdir(menu[current_row])
                current_row = 0
           elif os.path.isfile(menu[current_row]) == True:
               pygame.mixer.init()
               pygame.mixer.music.load(menu[current_row])
               pygame.mixer.music.play()
        elif key == curses.KEY_BACKSPACE:
            os.chdir("..")
            current_row = 0
        print_menu(stdscr, current_row)

'''
This function draws the menu and starts the navigation system. The cursor starts out at row 0.
'''
def draw_menu(stdscr):
    current_row = 0 
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    print_menu(stdscr, current_row)
    navigation(current_row, stdscr)

curses.wrapper(draw_menu) #initializes curses and calls function draw_menu

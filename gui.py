import pygame
from pygame import mixer
import os
from os import listdir
import curses
from math import *

def print_screen(stdscr, selected_row_idx, scroll_level):
    '''
    Takes the screen, current row and the scroll level as input and outputs the menu as well as 
    the cyan selection of the current row.
    '''
    stdscr.clear()
    
    height, width = stdscr.getmaxyx()
    max_rows = 15
    
    stdscr.border(0)
    box_menu = curses.newwin(height,width,0,0)
    box_menu.box()
    
    menu = os.listdir()
    menu_view = menu[scroll_level: scroll_level + max_rows + 1]
    
    box_menu.refresh()
    draw_menu(menu_view, scroll_level, stdscr, selected_row_idx)
    stdscr.refresh()

def draw_menu(menu_view, scroll_level, stdscr, selected_row_idx):
    '''
    This draws the menu and selection for the function print_screen
    '''
    height, width = stdscr.getmaxyx()
        
    for idx, row in enumerate(menu_view):
        x = width//2 - len(row)//2
        y = height//2 - len(menu_view)//2 + idx
        if idx == selected_row_idx -  scroll_level:
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


def navigation(current_row, stdscr):
    '''
    Function that takes the current row and the screen, and listens to key presses.
    This tells print_screen to update the screen depending on the user input.
    '''
    scroll_level = 0
    max_rows = 15 
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
            if current_row >= max_rows:
                scroll_level -= 1
            
        elif key == curses.KEY_DOWN and current_row < len(menu)-1:
            current_row += 1
            if current_row > max_rows:
                scroll_level += 1
                
        elif key == curses.KEY_ENTER or key in [10, 13]: 
           if os.path.isdir(menu[current_row]) == True:
                os.chdir(menu[current_row])
                current_row = 0
                scroll_level = 0
           elif os.path.isfile(menu[current_row]) == True:
               pygame.mixer.init()
               pygame.mixer.music.load(menu[current_row])
               pygame.mixer.music.play()
        elif key == curses.KEY_BACKSPACE:
            os.chdir("..")
            current_row = 0
        print_screen(stdscr, current_row, scroll_level)

def music_player(stdscr):    
    '''
    This function draws the menu and starts the navigation system. The cursor starts out at row 0.
    '''
    current_row = 0
    scroll_level = 0
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    print_screen(stdscr, current_row, scroll_level)
    navigation(current_row, stdscr)

curses.wrapper(music_player) #initializes curses and calls function draw_menu

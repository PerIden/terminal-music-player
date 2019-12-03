import pygame
from pygame import mixer
import os
from os import listdir
import curses
from math import *


class menu:
        def __init__(self, stdscr):
            self.stdscr = stdscr
            self.scroll_level = 0
            self.current_row = 0
            self.max_rows = 15
            self.menu = os.listdir()
            self.menu_view = self.menu[self.scroll_level: self.scroll_level + self.max_rows + 1]             
        def print_screen(self):
            self.stdscr.clear()
            self.height, self.width = self.stdscr.getmaxyx()
            
            self.stdscr.border(0)
            box_menu = curses.newwin(self.height,self.width,0,0)
            box_menu.box()
            box_menu.refresh()

            self.menu = os.listdir()
            self.menu_view = self.menu[self.scroll_level: self.scroll_level + self.max_rows + 1]

            self.stdscr.refresh()
            self.draw_menu()

        def draw_menu(self):    
            for idx, row in enumerate(self.menu_view):
                x = self.width//2 - len(row)//2
                y = self.height//2 - len(self.menu_view)//2 + idx
                if idx == self.current_row -  self.scroll_level:
                    self.stdscr.attron(curses.color_pair(1))
                    try:
                        self.stdscr.addstr(y, x, row)
                    except curses.error:
                        pass
                    self.stdscr.attroff(curses.color_pair(1))
                else:
                    try:
                        self.stdscr.addstr(y, x, row)
                    except curses.error:
                        pass
        def navigation(self):
            while 1:
                try:
                    curses.curs_set(0)
                except:
                    pass
                key = self.stdscr.getch()
                #menu = os.listdir()
                if key == curses.KEY_UP and self.current_row > 0:
                    self.current_row -= 1
                    if self.current_row >= self.max_rows:
                        self.scroll_level -= 1
            
                elif key == curses.KEY_DOWN and self.current_row < len(self.menu)-1:
                    self.current_row += 1
                    if self.current_row > self.max_rows:
                        self.scroll_level += 1
                
                elif key == curses.KEY_ENTER or key in [10, 13]: 
                    if os.path.isdir(self.menu[self.current_row]) == True:
                        os.chdir(self.menu[self.current_row])
                        self.current_row = 0
                        self.scroll_level = 0
                    elif os.path.isfile(self.menu[self.current_row]) == True:
                        pygame.mixer.init()
                        pygame.mixer.music.load(self.menu[self.current_row])
                        pygame.mixer.music.play()
                elif key == curses.KEY_BACKSPACE:
                    os.chdir("..")
                    self.current_row = 0

                elif key == ord('s') or key == curses.KEY_DOWN:
                    self.sort_menu()
                    self.menu = self.menu.sort
                    self.stdscr.refresh()
                self.print_screen()



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
#    current_row = 0
  #  scroll_level = 0
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    #print_screen(stdscr, current_row, scroll_level)
    #navigation(current_row, stdscr)
    menuObject = menu(stdscr)
    menuObject.print_screen()
    menuObject.navigation()
curses.wrapper(music_player) #initializes curses and calls function music_player

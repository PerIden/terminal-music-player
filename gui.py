import os
from os import listdir
import curses

def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    menu = os.listdir()
    height, width = stdscr.getmaxyx()
    stdscr.refresh()
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
            #current_row = idx
        else:
            try:
                stdscr.addstr(y, x, row)
            except curses.error:
                pass
        
    stdscr.refresh()

def main(stdscr):
    
    # specify the current selected row
    current_row = 0
    
    # print the menu
    print_menu(stdscr, current_row)
    menu = os.listdir()
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
            if len(menu) != 0:
                os.chdir(menu[current_row])
                current_row = 0
        elif key == curses.KEY_BACKSPACE:
            os.chdir("..")
            current_row = 0
        print_menu(stdscr, current_row)

curses.wrapper(main)

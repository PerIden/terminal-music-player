import pygame
from pygame import mixer
import os
from os import listdir
import curses
import vlc


class menu:
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.scroll_level = 0
        self.current_row = 0
        self.max_rows = 15
        self.menu = sorted(os.listdir())
        self.menu_view = self.menu[self.scroll_level: self.scroll_level + self.max_rows + 1]
        
    def print_screen(self):
        '''
        Takes the screen, current row and the scroll level as input and outputs the menu as well as the cyan selection of the current row.
        '''
        self.stdscr.clear()
        self.height, self.width = self.stdscr.getmaxyx()
            
        self.stdscr.border(0)
        box_menu = curses.newwin(self.height,self.width,0,0)
        box_menu.box()
        box_menu.refresh()

        self.menu = sorted(os.listdir())
        self.menu = self.menu
        self.menu_view = self.menu[self.scroll_level: self.scroll_level + self.max_rows + 1]

        self.stdscr.refresh()
        self.draw_menu()

    def draw_menu(self):
        '''
        This draws the menu and selection for the function print_screen
        '''
        
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
        '''
        Function that takes the current row and the screen, and listens to key presses.
        This tells print_screen to update the screen depending on the user input.
        '''
            
        while 1:
            try:
                curses.curs_set(0)
            except:
                pass
            key = self.stdscr.getch()
            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
                if self.current_row >= self.max_rows:
                    self.scroll_level -= 1
                        
            elif key == curses.KEY_DOWN and self.current_row < len(self.menu)-1:
                self.current_row += 1
                if self.current_row > self.max_rows:
                    self.scroll_level += 1
                        
            elif key == curses.KEY_ENTER or key in [10, 13]: 
                if os.path.isdir(self.menu[self.current_row]) == True: #Checks if the selected row is a directory
                    os.chdir(self.menu[self.current_row]) #Changes directory
                    self.current_row = 0
                    self.scroll_level = 0
                elif os.path.isfile(self.menu[self.current_row]) == True: #Checks if selected row is a file 
                    song_info = songs(self.menu, self.current_row)
                    song_info.play_song() #Plays the file
            elif key == curses.KEY_BACKSPACE:
                os.chdir("..")
                self.current_row = 0

            self.print_screen()


class songs(menu):

    def __init__(self, playlist, currently_playing):
        self.playlist = playlist
        self.currently_playing = currently_playing #for now this is an int
        self.Instance = vlc.Instance()

    def change_playlist(playlist, currently_playing):
        self.playlist = playlist
        self.currently_playing = currently_playing

    def next_song(self):
        self.currently_playing = self.currently_playing + 1
        self.play_song()

    def play_song(self):
        media_list = self.Instance.media_list_new(self.playlist)
        list_player = self.Instance.media_list_player_new()
        list_player.set_media_list(media_list)
        list_player.play()

def music_player(stdscr):    
    '''
    This function draws the menu and starts the navigation system. The cursor starts out at row 0.
    '''
    
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    menuObject = menu(stdscr)
    menuObject.print_screen()
    menuObject.navigation()
curses.wrapper(music_player) #initializes curses and calls function music_player

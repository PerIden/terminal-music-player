import os
from os import listdir
import curses
import vlc
from curses.textpad import Textbox, rectangle

class menu:
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.scroll_level = 0
        self.current_row = 0
        self.max_rows = 15 #Amount of rows to be displayed in the menu at once
        self.center_x = 6
        self.center_y = 4
        self.menu = sorted(os.listdir())
        self.menu_view = self.menu[self.scroll_level: self.scroll_level + self.max_rows + 1] #Only display 15 rows at once

    def type_box(self):
        '''
        Opens up a box that takes a user input string and saves it at userMessage, then exited with Ctrl + G
        '''
        
        editwin = curses.newwin(1, 73, self.max_rows + 9  , self.center_x) #Placing the textwindow
        self.stdscr.refresh()

        box = Textbox(editwin)
        box.edit()
        userMessage = box.gather()
        return userMessage

    def execute_user_input(self, message):
        if message.startswith('-default '):
            os.chdir(os.path.expanduser(message[9:-1])) #expanduser makes it possible to use ~ when changing directory
    
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

        self.menu = sorted(os.listdir()) #menu is sorted numerically 
        self.menu = self.menu
        self.menu_view = self.menu[self.scroll_level: self.scroll_level + self.max_rows + 1]

        self.stdscr.refresh()
        self.draw_menu()

    def draw_menu(self):
        '''
        This draws the menu and selection for the function print_screen
        '''
        
        for idx, row in enumerate(self.menu_view): #Places the text in the middle of the screen
            x = self.width//2 - self.center_x 
            y = self.height//2 - len(self.menu_view)//2 + idx
            if idx == self.current_row -  self.scroll_level:
                self.stdscr.attron(curses.color_pair(1)) #Highlights the selected row
                try:
                    self.stdscr.addstr(y, x, row)
                except curses.error:
                    pass
                self.stdscr.attroff(curses.color_pair(1))
            else:
                try:
                    self.stdscr.addstr(y, x, row) #Adds the other rows unselected
                except curses.error:
                    pass
                    
    def navigation(self):
        '''
        Function that takes the current row and the screen, and listens to key presses.
        This tells print_screen to update the screen depending on the user input.
        '''
            
        while 1:
            try: 
                curses.curs_set(0) #disabling cursor doesn't work for all terminals
            except:
                pass
            
            key = self.stdscr.getch() #Listens to the user input key
            
            if key == curses.KEY_UP and self.current_row > 0: 
                self.current_row -= 1
                if self.current_row == self.scroll_level - 1 and self.current_row >= 0: #Scrolls the menu up one step if the cursor is at the top of the menu
                    self.scroll_level -= 1
                        
            elif key == curses.KEY_DOWN and self.current_row < len(self.menu)-1:
                self.current_row += 1
                if self.current_row == self.scroll_level + self.max_rows + 1 and self.current_row < len(self.menu): #Scrolls the menu down one step if the cursor is at the bottom of the menu
                    self.scroll_level += 1
                        
            elif key == curses.KEY_ENTER or key in [10, 13]: 
                if os.path.isdir(self.menu[self.current_row]) == True: #Checks if the selected row is a directory
                    os.chdir(self.menu[self.current_row]) #Changes directory
                    self.current_row = 0
                    self.scroll_level = 0
                elif os.path.isfile(self.menu[self.current_row]) == True: #Checks if selected row is a file 
                    song_info = songs(self.menu, self.current_row) #Creates an instance of the songs of the directory
                    song_info.play_song() #Plays the song
            elif key == curses.KEY_BACKSPACE:
                os.chdir("..") #Changes directory to parent directory
                self.current_row = 0
            elif key == ord('a'):
                message = self.type_box()
                self.execute_user_input(message)
            elif key == ord('p'):
                try:
                    song_info.pause()
                except:
                    pass
                

            self.print_screen()


class songs(menu):

    def __init__(self, playlist, currently_playing):
        self.playlist = playlist
        self.currently_playing = currently_playing #for now this is an int
        self.Instance = vlc.Instance()

    def change_playlist(playlist, currently_playing):
        self.playlist = playlist
        self.currently_playing = currently_playing

    def pause_song(self):
        self.list_player.pause()
        
    def play_song(self):
        '''
        Play the playlist from the current position you are at.
        '''
        try:
            media_list = self.Instance.media_list_new(self.playlist) #Loads the files in the directory
            self.list_player = self.Instance.media_list_player_new()
            self.list_player.set_media_list(media_list)
            self.list_player.play() #Plays all the files in the directory one after the other
        except vlc.error:
            pass

def music_player(stdscr):    
    '''
    This function draws the menu and starts the navigation system. The cursor starts out at row 0.
    '''
    
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    menuObject = menu(stdscr)
    menuObject.print_screen()
    menuObject.navigation()
curses.wrapper(music_player) #initializes curses and calls function music_player

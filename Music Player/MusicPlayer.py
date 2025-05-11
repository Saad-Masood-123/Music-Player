from tkinter import filedialog, Menu, Listbox, PhotoImage, Frame, Button, Tk, END
import pygame
import os

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("500x300")
        pygame.mixer.init()
        
        self.songs = []
        self.current_song = ""
        self.paused = False
        
        self.setup_ui()
    
    def setup_ui(self):
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        
        self.organise_menu = Menu(self.menubar, tearoff=False)
        self.organise_menu.add_command(label='Select Folder', command=self.load_music)
        self.menubar.add_cascade(label='Organise', menu=self.organise_menu)
        
        self.songlist = Listbox(self.root, bg="black", fg="white", width=100, height=15)
        self.songlist.pack()
        
        self.play_btn_image = PhotoImage(file='play.png')
        self.pause_btn_image = PhotoImage(file='pause.png')
        self.next_btn_image = PhotoImage(file='next.png')
        self.prev_btn_image = PhotoImage(file='previous.png')
        
        self.control_frame = Frame(self.root)
        self.control_frame.pack()
        
        self.play_btn = Button(self.control_frame, image=self.play_btn_image, borderwidth=0, command=self.play_music)
        self.pause_btn = Button(self.control_frame, image=self.pause_btn_image, borderwidth=0, command=self.pause_music)
        self.next_btn = Button(self.control_frame, image=self.next_btn_image, borderwidth=0, command=self.next_music)
        self.prev_btn = Button(self.control_frame, image=self.prev_btn_image, borderwidth=0, command=self.prev_music)
        
        self.play_btn.grid(row=0, column=1, padx=7, pady=10)
        self.pause_btn.grid(row=0, column=2, padx=7, pady=10)
        self.next_btn.grid(row=0, column=3, padx=7, pady=10)
        self.prev_btn.grid(row=0, column=0, padx=7, pady=10)
    
    def load_music(self):
        self.root.directory = filedialog.askdirectory()
        for song in os.listdir(self.root.directory):
            name, ext = os.path.splitext(song)
            if ext == '.mp3':
                self.songs.append(song)
        self.songlist.delete(0, END)
        for song in self.songs:
            self.songlist.insert("end", song)
        if self.songs:
            self.songlist.selection_set(0)
            self.current_song = self.songs[self.songlist.curselection()[0]]
    
    def play_music(self):
        if self.songs and not self.paused:
            try:
                self.current_song = self.songs[self.songlist.curselection()[0]]
                pygame.mixer.music.load(os.path.join(self.root.directory, self.current_song))
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Error playing music: {e}")
        elif self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
    
    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.paused = True
    
    def next_music(self):
        try:
            current_index = self.songs.index(self.current_song)
            next_index = (current_index + 1) % len(self.songs)
            self.songlist.selection_clear(0, END)
            self.songlist.selection_set(next_index)
            self.current_song = self.songs[next_index]
            self.play_music()
        except Exception as e:
            print(f"Error selecting next music: {e}")
    
    def prev_music(self):
        try:
            current_index = self.songs.index(self.current_song)
            prev_index = (current_index - 1) % len(self.songs)
            self.songlist.selection_clear(0, END)
            self.songlist.selection_set(prev_index)
            self.current_song = self.songs[prev_index]
            self.play_music()
        except Exception as e:
            print(f"Error selecting previous music: {e}")

if __name__ == "__main__":
    root = Tk()
    app = MusicPlayer(root)
    root.mainloop()

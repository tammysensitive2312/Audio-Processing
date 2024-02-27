import pygame
import tkinter as tk
from functools import partial


pygame.init()
pygame.mixer.init()

def play_sound(sound_file):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

root = tk.Tk()
root.title("Soundboard")


sound_files = [
    r"C:\Users\ACER\Documents\Zalo Received Files\sound\8d82b5_Tom_and_Jerry_Cuckoo_Clock_Sound_Effect.mp3",
    r"C:\Users\ACER\Documents\Zalo Received Files\sound\8d82b5_Tom_and_Jerry_Gelatine_Sound_Effect.mp3",
    r"C:\Users\ACER\Documents\Zalo Received Files\sound\8d82b5_Tom_and_Jerry_Prick_Sound_Effect.mp3",
    r"C:\Users\ACER\Documents\Zalo Received Files\sound\8d82b5_Tom_and_Jerry_Prick_Sound_FX.mp3",
    r"C:\Users\ACER\Documents\Zalo Received Files\sound\8d82b5_Tom_and_Jerry_Robot_Cat_Sound_Effect.mp3",
    r"C:\Users\ACER\Documents\Zalo Received Files\sound\8d82b5_Tom_Laughing_Sound_Effect.mp3",
    r"C:\Users\ACER\Documents\Zalo Received Files\sound\8d82b5_Tom_Scream_Sound_Effect.mp3",
    r"C:\Users\ACER\Documents\Zalo Received Files\sound\bones-scream-funny-152222.mp3",
    r"C:\Users\ACER\Documents\Zalo Received Files\sound\echo-pop-1-189792.mp3",
    r"C:\Users\ACER\Documents\Zalo Received Files\sound\yeah-boy-114748.mp3",
    r"C:\Users\ACER\Documents\Zalo Received Files\sound\wowowowowowowow-103214.mp3",
    r"C:\Users\ACER\Documents\Zalo Received Files\sound\wow-121578.mp3",
    r"C:\Users\ACER\Documents\Zalo Received Files\sound\waterphone-174768.mp3",
    r"C:\Users\ACER\Documents\Zalo Received Files\sound\kicking-screams-152223.mp3",
    r"C:\Users\ACER\Documents\Zalo Received Files\sound\guitar-riff-159089.mp3",
    r"C:\Users\ACER\Documents\Zalo Received Files\sound\fart-145914.mp3"
]


for index, sound_file in enumerate(sound_files, start=1):
    button_text = f"Sound {index}"
    button = tk.Button(root, text=button_text, command=partial(play_sound, sound_file))
    button.pack(pady=5, padx=10, side='top', fill='x')

root.mainloop()
pygame.quit()

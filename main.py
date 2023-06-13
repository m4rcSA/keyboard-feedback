import sys
import pygame
from pynput import keyboard
from pynput.keyboard import Key
import random

import click


# Load the sound
enter = None

keys = []

def init(device="mechanical"):
    global enter, keys
    pygame.mixer.init()
    enter = pygame.mixer.Sound(f"assets/{device}/enter_click.wav")
    for i in range(1,7):
        keys.append(pygame.mixer.Sound(f"assets/{device}/key_{i}.wav"))

def play_key(key):

    if key==Key.enter:
        enter.play()
    elif key:
        random.choice(keys).play()
    else:
        enter.play()

@click.command()
@click.option('-t', '--typewriter', is_flag=True)
def main(typewriter):
    click.echo("Press CTRL + Esc to exit")
    if typewriter:
        init("typewriter")
    else:
        init()

    # Create a listener for the keyboard
    listener = keyboard.Listener(on_press=play_key)
    listener.start()  # start the listener
    listener.join()  # join the listener thread to the main thread to keep waiting for keys


if __name__ == '__main__':
    main()
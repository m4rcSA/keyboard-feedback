import sys
import pygame
from pynput import keyboard
from pynput.keyboard import Key
import random

import click


# Load the sound
enter = None

keys = []
pressed_keys = set()

def init(device="mechanical"):
    global enter, keys
    pygame.mixer.init()
    enter = pygame.mixer.Sound(f"assets/{device}/enter_click.wav")
    for i in range(1, 7):
        keys.append(pygame.mixer.Sound(f"assets/{device}/key_{i}.wav"))

def play_key(key):
    if key == Key.enter:
        if Key.enter not in pressed_keys:
            pressed_keys.add(Key.enter)
            enter.play()
    elif key and key not in pressed_keys:
        pressed_keys.add(key)
        random.choice(keys).play()

def release_key(key):
    if key in pressed_keys:
        pressed_keys.remove(key)

@click.command()
@click.option('-t', '--typewriter', is_flag=True)
def main(typewriter):
    click.echo("Press CTRL + Esc to exit")
    if typewriter:
        init("typewriter")
    else:
        init()

    # Create a listener for the keyboard
    with keyboard.Listener(on_press=play_key, on_release=release_key) as listener:
        listener.join()  # join the listener thread to the main thread to keep waiting for keys


if __name__ == '__main__':
    main()

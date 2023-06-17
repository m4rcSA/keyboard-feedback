import sys
import pygame
import keyboard
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

def play_key(event, repeat_allowed=True):
    if event.name == "enter":
        if repeat_allowed or event.name not in pressed_keys:
            pressed_keys.add(event.name)
            enter.play()
    elif event.name and (repeat_allowed or event.name not in pressed_keys):
        pressed_keys.add(event.name)
        random.choice(keys).play()

def release_key(event):
    if event.name in pressed_keys:
        pressed_keys.remove(event.name)

@click.command()
@click.option('-s', '--sound', type=str, default='mechanical', help='Specify the soundpack (e.g., mechanical, typewriter)')
@click.option('-r', '--repeat', is_flag=True, help='Enable key repeat')
def main(sound, repeat):
    click.echo("Press CTRL + C to exit")
    init(sound)

    # Create keyboard hooks
    keyboard.on_press(lambda event: play_key(event, repeat), suppress=True)
    keyboard.on_release(lambda event: release_key(event), suppress=True)

    # Keep the script running until CTRL + c is pressed
    keyboard.wait()

if __name__ == '__main__':
    main()

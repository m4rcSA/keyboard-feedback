import sys
import pygame
import keyboard
import json
import click

# Load the sound
key_sounds = {}
pressed_keys = set()

def init(device_sound="nk-cream"):
    global key_sounds

    config_file = f"assets/{device_sound}/config.json"
    with open(config_file) as f:
        config = json.load(f)

    pygame.mixer.init()
    for key, value in config['defines'].items():
        if value is not None:
            key_sounds[int(key)] = pygame.mixer.Sound(f"assets/{device_sound}/{value}")

def play_key(event, repeat_allowed=True):
    if event.scan_code in key_sounds and (repeat_allowed or event.scan_code not in pressed_keys):
        pressed_keys.add(event.scan_code)
        key_sounds[event.scan_code].play()

def release_key(event):
    if event.scan_code in pressed_keys:
        pressed_keys.remove(event.scan_code)

@click.command()
@click.option('-s', '--device-sound', type=str, default='nk-cream', help='Specify the device sound folder name')
@click.option('-r', '--repeat', is_flag=True, help='Enable key repeat')
def main(device_sound, repeat):
    click.echo("Press CTRL + C to exit")
    init(device_sound)

    # Create keyboard hooks
    keyboard.on_press(lambda event: play_key(event, repeat), suppress=True)
    keyboard.on_release(lambda event: release_key(event), suppress=True)

    # Keep the script running indefinitely
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()

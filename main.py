import sys
import pygame
from pynput import keyboard
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

def play_key(key, repeat_allowed=True, print_scan_code=False):
    scan_code = getattr(key, 'scan_code', None)
    if scan_code is not None and scan_code in key_sounds and (repeat_allowed or scan_code not in pressed_keys):
        pressed_keys.add(scan_code)
        key_sounds[scan_code].play()
    if print_scan_code:
        print(f"Scan code: {scan_code}")

def release_key(key):
    scan_code = getattr(key, 'scan_code', None)
    if scan_code is not None and scan_code in pressed_keys:
        pressed_keys.remove(scan_code)

@click.command()
@click.option('-s', '--device-sound', type=str, default='nk-cream', help='Specify the device sound folder name')
@click.option('-r', '--repeat', is_flag=True, help='Enable key repeat')
@click.option('-p', '--print-scan-code', is_flag=True, help='Print the scan code of the pressed key')
def main(device_sound, repeat, print_scan_code):
    click.echo("Press CTRL + C to exit")
    init(device_sound)

    # Create keyboard listener
    listener = keyboard.Listener(
        on_press=lambda key: play_key(key, repeat, print_scan_code),
        on_release=lambda key: release_key(key)
    )
    listener.start()

    # Keep the script running indefinitely
    try:
        listener.join()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()

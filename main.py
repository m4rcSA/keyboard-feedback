import sys
from pygame import mixer
from pynput import keyboard
import json
import click
import random
from os import path

# Load the sound
key_sounds = {}
pressed_keys = set()

def init(device_sound="nk-cream"):
    global key_sounds

    if path.isdir(device_sound):
        sound_folder = device_sound
    else:
        sound_folder = f"assets/{device_sound}"

    config_file = path.join(sound_folder, "config.json")
    with open(config_file) as f:
        config = json.load(f)

    mixer.init()
    for key, value in config['defines'].items():
        if value is not None:
            key_sounds[int(key)] = mixer.Sound(f"assets/{device_sound}/{value}")

def play_key(key, repeat_allowed=False, print_scan_code=False, debug=False):
    try:
        scan_code = key.vk
        if debug:
            click.echo(f"key.vk {scan_code}")
    except AttributeError:
        scan_code = key.value.vk
        if debug:
            click.echo(f"key.value.vk {scan_code}")

    if scan_code in key_sounds and (repeat_allowed or scan_code not in pressed_keys):
        if debug:
            click.echo("key found")
        pressed_keys.add(scan_code)
        key_sounds[scan_code].play()
    elif repeat_allowed or scan_code not in pressed_keys:
        pressed_keys.add(scan_code)
        random.choice(list(key_sounds.values())).play()

    if print_scan_code:
        click.echo(f"Scan code: {scan_code}")

def release_key(key,debug=False):
    try:
        scan_code = key.vk
        if debug:
            click.echo(f"key.vk {scan_code}")
    except AttributeError:
        scan_code = key.value.vk
        if debug:
            click.echo(f"key.value.vk {scan_code}")
    
    if scan_code is not None and scan_code in pressed_keys:
        pressed_keys.remove(scan_code)

@click.command()
@click.option('-s', '--device-sound', type=str, default='nk-cream', help='Specify the device sound folder name')
@click.option('-r', '--repeat', is_flag=True, help='Enable key repeat')
@click.option('-p', '--print-scan-code', is_flag=True, help='Print the scan code of the pressed key')
@click.option('-d', '--debug', is_flag=True, help='Enable debug output')
def main(device_sound, repeat, print_scan_code, debug):
    click.echo("Press CTRL + C to exit")
    init(device_sound)

    # Create keyboard listener
    listener = keyboard.Listener(
        on_press=lambda key: play_key(key, repeat, print_scan_code, debug),
        on_release=lambda key: release_key(key, debug)
    )
    listener.start()

    # Keep the script running indefinitely
    try:
        listener.join()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()

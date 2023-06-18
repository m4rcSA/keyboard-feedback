import sys
import pygame
import click
import subprocess
import json
import re
import threading

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

def play_key(scan_code, repeat_allowed=True):
    if scan_code in key_sounds and (repeat_allowed or scan_code not in pressed_keys):
        pressed_keys.add(scan_code)
        key_sounds[scan_code].play()

def process_libinput_output(output, repeat, debug):
    lines = output.strip().split('\n')
    for line in lines:
        if debug:
            click.echo(line)  # Print the libinput event

        event_parts = line.strip().split()
        if len(event_parts) >= 5 and event_parts[1] == 'KEYBOARD_KEY':
            if event_parts[5] == 'pressed':
                match = re.search(r'\((\d+)\)', event_parts[4])
                if match:
                    scan_code = int(match.group(1))
                    play_key(scan_code, repeat)
            elif event_parts[5] == 'released':
                match = re.search(r'\((\d+)\)', event_parts[4])
                if match:
                    scan_code = int(match.group(1))
                    if scan_code in pressed_keys:
                        pressed_keys.remove(scan_code)

@click.command()
@click.option('-s', '--device-sound', type=str, default='nk-cream', help='Specify the device sound folder name')
@click.option('-r', '--repeat', is_flag=True, help='Enable key repeat')
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode to print libinput events')
def main(device_sound, repeat, debug):
    click.echo("Press CTRL + C to exit")
    init(device_sound)

    libinput_command = ['sudo', 'libinput', 'debug-events', '--show-keycodes', '--device', '/dev/input/event3']
    libinput_process = subprocess.Popen(libinput_command, stdout=subprocess.PIPE, universal_newlines=True)

    def read_libinput_output():
        while True:
            output = libinput_process.stdout.readline()
            if not output:
                break
            process_libinput_output(output, repeat, debug)

    # Start a separate thread to read libinput output
    libinput_thread = threading.Thread(target=read_libinput_output)
    libinput_thread.start()

    try:
        while True:
            pass  # Keep the main thread running

    except KeyboardInterrupt:
        libinput_process.kill()
        libinput_thread.join()

if __name__ == '__main__':
    main()

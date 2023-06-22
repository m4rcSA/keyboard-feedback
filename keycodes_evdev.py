from pathlib import Path
from evdev import InputDevice, ecodes

def store_pressed_keycodes(output_file):
    # Keycode storage
    key_pairs = []

    # Find the input device
    devices = [InputDevice(path) for path in Path('/dev/input').rglob('event3')]
    device = None

    for dev in devices:
        if 'keyboard' in dev.name.lower():
            device = dev
            break

    if device is None:
        print("No keyboard device found.")
        return

    print(f"Using keyboard device: {device.name}")

    # Capture keycodes
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            keycode = event.code
            key_value = ecodes.KEY[keycode]

            if key_value != 'KEY_UNKNOWN':
                key_pairs.append((key_value, keycode))

        if len(key_pairs) >= 10:
            # Capture 10 keycodes and stop
            break

    # Create the output file
    with open(output_file, 'w') as f:
        # Write the import statement and key pairs
        f.write("from evdev import ecodes\n\n")
        f.write("key_pairs = [\n")

        # Write the key pairs
        for key_value, keycode in key_pairs:
            f.write(f"    ('{key_value}', {keycode}),\n")

        # Write the closing bracket
        f.write("]\n")

    print(f"Character and Keycode pairs stored in: {output_file}")

# Example usage
output_file = 'key_pairs.py'
store_pressed_keycodes(output_file)

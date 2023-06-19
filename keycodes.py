from pathlib import Path
from pynput import keyboard

def store_pressed_keycodes(output_file):
    # Keycode storage
    key_pairs = []

    def on_press(key):
        nonlocal key_pairs

        if hasattr(key, 'vk'):
            keycode = key.vk
            key_value = key.char
        elif hasattr(key, 'value'):
            keycode = key.value.vk
            key_value = key.name

        if keycode is not None and key_value is not None:
            key_pairs.append((key_value, keycode))

    def on_release(key):
        if key == keyboard.Key.esc:
            # Stop listener on ESC key
            return False

    # Create and start the listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    # Wait for the listener to stop
    listener.join()

    # Create the output file
    with open(output_file, 'w') as f:
        # Write the import statement and key pairs
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

from pynput import keyboard

def on_activated():
    print("Shortcut pressed")

def start_listening():
    with keyboard.GlobalHotKeys({
        "<ctrl>+<alt>+h": on_activated
    }) as h:
    h.start()
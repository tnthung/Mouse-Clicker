from os             import system
from sys            import stdout
from time           import sleep
from importlib.util import find_spec


# Check if pynput is installed
if not find_spec("pynput"): system("pip install pynput")
from pynput.mouse    import Button, Controller
from pynput.keyboard import Key   , Listener


# Shortcuts
QUIT_KEY     = Key.scroll_lock
TOGGLE_KEY   = Key.pause
INCREASE_KEY = Key.up
DECREASE_KEY = Key.down
BUTTON_LEFT  = Key.left
BUTTON_RIGHT = Key.right


# Initialize
ALIVE         = True
CLICK         = False
CLICK_BUTTON  = Button.left
CLICK_PER_SEC = 1


def update():
    stdout.write(f"\033[2K\033[E\033[A")
    stdout.write(f"CPS: {CLICK_PER_SEC:>3} | ")
    stdout.write(f"Button: {CLICK_BUTTON.name:>5} | ")
    stdout.write(f"State: {'ON' if CLICK else 'OFF'}")
    stdout.flush()


# keyboard listener
def on_press(key):
    global CLICK, TOGGLE_KEY, CLICK_BUTTON, CLICK_PER_SEC, ALIVE

    if (key == TOGGLE_KEY):
        CLICK = not CLICK

    elif (key == INCREASE_KEY):
        CLICK_PER_SEC += 1

    elif (key == DECREASE_KEY):
        if CLICK_PER_SEC > 1: 
            CLICK_PER_SEC -= 1

    elif (key == BUTTON_LEFT):
        CLICK_BUTTON = Button.left

    elif (key == BUTTON_RIGHT):
        CLICK_BUTTON = Button.right

    elif (key == QUIT_KEY):
        ALIVE = False

    update()


def main():
    global CLICK, TOGGLE_KEY, CLICK_BUTTON, CLICK_PER_SEC, ALIVE

    stdout.write(f"\033[H\033[J")
    stdout.write(f"Quit  : [{QUIT_KEY  .name.upper()}]\n")
    stdout.write(f"Toggle: [{TOGGLE_KEY.name.upper()}]\n")
    update()
    Listener(on_press=on_press).start()

    # Mouse controller
    mouse = Controller()

    # Loop
    try:
        while ALIVE:
            if CLICK: mouse.click(CLICK_BUTTON)
            sleep(1 / CLICK_PER_SEC)

    except KeyboardInterrupt: pass


if __name__ == "__main__": main()

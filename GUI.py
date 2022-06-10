import tkinter as tk

from os             import system
from time           import sleep, time
from threading      import Thread
from importlib.util import find_spec


if not find_spec("pynput"): system("pip3 install pynput")
from pynput.mouse    import Button, Controller
from pynput.keyboard import Key   , Listener


# Shortcuts
QUIT_KEY     = Key.scroll_lock
TOGGLE_KEY   = Key.pause
INCREASE_KEY = Key.up
DECREASE_KEY = Key.down
BUTTON_LEFT  = Key.left
BUTTON_RIGHT = Key.right


class Main:
    def __init__(self):
        self.root = tk.Tk()

        self.cps    = 1
        self.alive  = True
        self.state  = False
        self.button = Button.left

        self.stringVarInput  = tk.StringVar()
        self.stringVarToggle = tk.StringVar()

        self.mouse = Controller()

        self.setup()
        self.run()

    # run
    def run(self):
        self.lis  = Listener(on_press=self.on_press )
        self.loop = Thread  (target  =self.clickLoop)

        self.lis .start()
        self.loop.start()

        self.root.mainloop()

    def clickLoop(self):
        while self.alive:
            if self.state and self.cps > 0: 
                self.mouse.click(self.button)
            
            self.sleep(1 / self.cps)

    # helper
    def sleep(self, sec):
        while sec > 0:
            tmp = 0.25 if sec > 0.25 else sec
            sleep(tmp)
            if not self.alive: return
            sec -= tmp


    # handler
    def on_press(self, key):
        if   key == QUIT_KEY    : self.quit()
        elif key == TOGGLE_KEY  : self.toggle()
        elif key == INCREASE_KEY: self.increase()
        elif key == DECREASE_KEY: self.decrease()
        elif key == BUTTON_LEFT : self.switch_left()
        elif key == BUTTON_RIGHT: self.switch_right()

    def on_change(self, *_):
        sv = self.stringVarInput.get()

        if (sv != "" and not sv.isdecimal()):
            return self.stringVarInput.set(str(self.cps))

        self.cps = int(sv) if sv != "" else 0

    # action
    def increase(self):
        self.cps += 1
        self.stringVarInput.set(str(self.cps))

    def decrease(self):
        if self.cps > 1:
            self.cps -= 1
        self.stringVarInput.set(str(self.cps))

    def quit(self):
        self.alive = False

        self.lis .stop()
        self.loop.join()
        self.root.destroy()

    def toggle(self):
        self.state = not self.state
        self.stringVarToggle.set("Turn " + 
            ("OFF" if self.state else "ON") +
            f"  ({TOGGLE_KEY.name})")

    def switch_left(self):
        self.button = Button.left
        self.l.select()
        self.r.selection_clear()


    def switch_right(self):
        self.button = Button.right
        self.l.selection_clear()
        self.r.select()

    # setup GUI
    def setup(self):
        # setup var
        self.stringVarInput.set("1")
        self.stringVarInput.trace_add("write", self.on_change)

        self.stringVarToggle.set("Turn ON" + 
            f"  ({TOGGLE_KEY.name})")

        # root
        self.root.title    ("Mouse Clicker")
        self.root.protocol ("WM_DELETE_WINDOW", self.quit)
        self.root.resizable(False, False)

        # frames
        topLevelFrame = tk.LabelFrame(self.root, text="Mouse Clicker")
        topLevelFrame.pack(fill="both", expand=True, padx=5, pady=5)

        buttonSelectFrame = tk.Frame(topLevelFrame)
        buttonSelectFrame.pack(side=tk.TOP, fill=tk.X, padx=5)

        cpsSelectFrame = tk.Frame(topLevelFrame)
        cpsSelectFrame.pack(side=tk.TOP, fill=tk.X, padx=5)

        # toggle button
        tk.Button(
            topLevelFrame, 
            command     =self.toggle,
            textvariable=self.stringVarToggle,
        ).pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # button select
        self.l = tk.Radiobutton(buttonSelectFrame, text="Left" , value=0, command=self.switch_left )
        self.r = tk.Radiobutton(buttonSelectFrame, text="Right", value=1, command=self.switch_right)

        self.l.grid(row=0, column=1, padx=23, sticky="nsew")
        self.r.grid(row=0, column=2, padx=23, sticky="nsew")

        self.l.select()
        self.r.selection_clear()

        # cps select
        tk.Label(cpsSelectFrame, text="CPS:")\
            .grid(row=0, column=0, rowspan=2, sticky="nsew")

        i = tk.Entry(cpsSelectFrame, width=24, textvariable=self.stringVarInput)
        i.grid(row=0, column=1, rowspan=2, sticky="nsew")
        i.grid_columnconfigure(1, weight=2)

        tk.Button(cpsSelectFrame, text="▲", font=("Arial", 5), command=self.increase)\
            .grid(row=0, column=2, sticky="nsew")

        tk.Button(cpsSelectFrame, text="▼", font=("Arial", 5), command=self.decrease)\
            .grid(row=1, column=2, sticky="nsew")


if __name__ == "__main__": Main()

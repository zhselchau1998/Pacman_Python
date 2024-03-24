from pynput import keyboard

class KeyListener:
    def __init__(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.buffer = ''

        self.listener.start()
        
    def nextKey(self):
        if len(self.buffer) > 0:
            return self.buffer

    def on_press(self, key):
        try:
            k = key.char
        except:
            k = key.name
        if k in ['w','W','up']:# and 'w' not in self.buffer:     # Up keys
            self.buffer = 'w'
        if k in ['a','A','left']:# and 'a' not in self.buffer:   # Left keys
            self.buffer = 'a'
        if k in ['s','S','down']:# and 's' not in self.buffer:   # Down keys
            self.buffer = 's'
        if k in ['d','D','right']:# and 'd' not in self.buffer:  # Right keys
            self.buffer = 'd'
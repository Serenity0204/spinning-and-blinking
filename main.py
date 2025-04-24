import tkinter as tk
import tkinter.ttk as ttk
from serial import Serial
from serial.tools.list_ports import comports
from threading import Thread, Lock # we'll use Lock later ;)

def detached_callback(f):
    return lambda *args, **kwargs: Thread(target=f, args=args, kwargs=kwargs).start()

class LockedSerial(Serial):
    _lock: Lock = Lock()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def read(self, size=1) -> bytes:
        with self._lock:
            return super().read(size)

    def write(self, b: bytes, /) -> int | None:
        with self._lock:
            super().write(b)

    def close(self):
        with self._lock:
            super().close()

class App(tk.Tk):
    ser: LockedSerial

    def __init__(self):
        super().__init__()

        self.title("Motor Toggler")
        
        self.geometry("300x200")
       
        self.port = tk.StringVar() # add this
        self.state = 0
        self.direction = True  # True for Clockwise, False for Counter-Clockwise


        ttk.Checkbutton(self, text='Toggle Motor', command=self.toggle_motor).pack()
        ttk.Button(self, text='Disconnect', command=self.disconnect, default='active').pack()

        # Slider value label
        self.slider_value = tk.DoubleVar(value=26)
        self.slider_label = ttk.Label(self, text=f"Value: {self.slider_value.get():.0f}")
        self.slider_label.pack(pady=5)

        # Slide bar
        self.slider = ttk.Scale(
            self,
            from_=1,
            to=156,
            orient='horizontal',
            variable=self.slider_value,
            command=self.update_slider_label
        )
        self.slider.pack(fill='x', padx=20, pady=5)
        
        
        # Direction label and toggle button
        self.direction_label = ttk.Label(self, text="Direction: Clockwise")
        self.direction_label.pack(pady=5)
        ttk.Button(self, text="Toggle Direction", command=self.toggle_direction).pack()
        
        SerialPortal(self) # and this

    # and finally this
    def connect(self):
        self.ser = Serial(self.port.get())

    def disconnect(self):
        self.ser.close()
        SerialPortal(self) # display portal to reconnect

    @detached_callback
    def toggle_motor(self):
        self.state = not self.state
        if self.state:
            self.ser.write(bytes([0x1, int(self.slider_value.get()) + 99, int(self.direction)]))        
        else:
            self.ser.write(bytes([0x0, int(self.slider_value.get()) + 99, int(self.direction)]))

    @detached_callback
    def toggle_direction(self):
        self.direction = not self.direction
        direction_text = "Clockwise" if self.direction else "Counter-Clockwise"
        self.direction_label.config(text=f"Direction: {direction_text}")
        if self.state:
            self.ser.write(bytes([0x1, int(self.slider_value.get()) + 99, int(self.direction)]))   

    @detached_callback
    def update_slider_label(self, value):
        self.slider_label.config(text=f"Value: {float(value):.0f}")
        if self.state:
            self.ser.write(bytes([0x1, int(self.slider_value.get()) + 99, int(self.direction)]))   

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.disconnect()

class SerialPortal(tk.Toplevel):
    def __init__(self, parent: App):
        super().__init__(parent)

        self.parent = parent
        self.parent.withdraw() # hide App until connected

        ttk.OptionMenu(self, parent.port, '', *[d.device for d in comports()]).pack()
        ttk.Button(self, text='Connect', command=self.connect, default='active').pack()

    def connect(self):
        self.parent.connect()
        self.destroy()
        self.parent.deiconify() # reveal App



if __name__ == '__main__':
    app = App()
    app.mainloop()
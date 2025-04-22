import tkinter as tk
import tkinter.ttk as ttk
from serial import Serial
from serial.tools.list_ports import comports


class App(tk.Tk):
    ser: Serial

    def __init__(self):
        super().__init__()

        self.title("Motor Toggler")
        
        self.geometry("300x200")
       
        self.port = tk.StringVar() # add this
        self.state = 0

        ttk.Checkbutton(self, text='Toggle Motor', command=self.toggle_motor).pack()
        ttk.Button(self, text='Disconnect', command=self.disconnect, default='active').pack()

        SerialPortal(self) # and this

    # and finally this
    def connect(self):
        self.ser = Serial(self.port.get())

    def disconnect(self):
        self.ser.close()
        SerialPortal(self) # display portal to reconnect

    def toggle_motor(self):
        self.state = not self.state
        if self.state:
            self.ser.write(bytes([0x1]))
        else:
            self.ser.write(bytes([0x0]))
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
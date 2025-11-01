import threading
import time
from pynput import mouse, keyboard
import tkinter as tk
from tkinter import ttk

clicking = False
click_speed = 20  # 初期CPS
mouse_controller = mouse.Controller()

# クリックループ
def click_loop():
    global clicking
    while True:
        if clicking:
            mouse_controller.press(mouse.Button.left)
            mouse_controller.release(mouse.Button.left)
        time.sleep(1 / max(1, click_speed))

# F8 / ESC キー監視
def on_press(key):
    global clicking
    try:
        if key == keyboard.Key.f8:
            clicking = not clicking
            status_label.config(text=f"Status: {'ON' if clicking else 'OFF'}")
        elif key == keyboard.Key.esc:
            root.destroy()
            return False  # listener終了
    except AttributeError:
        pass

keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()

# GUI作成
def set_speed(value):
    global click_speed
    click_speed = float(value)
    speed_label.config(text=f"CPS: {int(click_speed)}")

root = tk.Tk()
root.title("AutoClicker (Toggle Mode)")
root.geometry("300x180")

status_label = ttk.Label(root, text="Status: OFF", font=("Arial", 12))
status_label.pack(pady=10)

speed_label = ttk.Label(root, text=f"CPS: {click_speed}")
speed_label.pack()

speed_slider = ttk.Scale(root, from_=1, to=60, orient="horizontal", command=set_speed)
speed_slider.set(click_speed)
speed_slider.pack(fill="x", padx=20, pady=10)

info_label = ttk.Label(root, text="F8 → Toggle Start/Stop\nESC → Exit")
info_label.pack(pady=10)

# クリックスレッド開始
threading.Thread(target=click_loop, daemon=True).start()

root.mainloop()


"""Automate FL Studio to open a drum project before starting a drumming session"""

import os
import subprocess
import time
import pyautogui
import sys


FL_STUDIO_PATH = os.getenv("FL_STUDIO_PATH", "FL Studio 2024")
PROJECT_NAME = os.getenv("FL_PROJECT_NAME", "DRUMS.flp")
WAIT_TIME = int(
    os.getenv("FL_WAIT_TIME", "5")
)  # seconds to wait for FL Studio to launch


def launch_fl_studio():
    """Launch FL Studio using the configured path."""
    print("[INFO] Launching FL Studio...")
    subprocess.Popen(["open", "-a", FL_STUDIO_PATH])
    time.sleep(WAIT_TIME)
    print("[INFO] FL Studio should be running now.")


def open_drum_project_pyautogui():

    print("Opening drum project...")
    # Open drum projet by clicking opt+1
    pyautogui.keyDown("command")
    pyautogui.press("o")
    pyautogui.keyUp("command")
    time.sleep(1)

    # Click search
    pyautogui.keyDown("command")
    pyautogui.press("f")
    pyautogui.keyUp("command")
    time.sleep(1)

    # Type project name
    pyautogui.typewrite(PROJECT_NAME)
    time.sleep(2)

    # Click project icon
    pyautogui.moveTo(568, 217)
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(0.2)

    # Open project
    pyautogui.moveTo(1080, 900)
    pyautogui.click()
    time.sleep(5)

    print("Opening EZD3...")
    # Open file in EZD3
    pyautogui.moveTo(190, 240)
    pyautogui.click()
    time.sleep(0.5)

    # Hoover open recent
    pyautogui.moveTo(200, 350)
    time.sleep(0.5)

    # Open most recent save
    pyautogui.moveTo(520, 350)
    pyautogui.click()
    time.sleep(0.5)

    # Dont save
    pyautogui.moveTo(785, 640)
    pyautogui.click()

    print("Done")


def open_drum_session():
    launch_fl_studio()
    open_drum_project_pyautogui()


if __name__ == "__main__":
    open_drum_session()

    print("Move your mouse to the desired location. Press Ctrl+C to exit.\n")

    try:
        while True:
            x, y = pyautogui.position()
            # Print coordinates on the same line
            print(f"\rMouse position: X={x} Y={y}   ", end="")
            sys.stdout.flush()
            time.sleep(0.05)  # Update every 50ms
    except KeyboardInterrupt:
        print("\n[INFO] Exiting mouse coordinate tracker.")

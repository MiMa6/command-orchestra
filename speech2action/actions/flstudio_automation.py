"""Automate FL Studio to open a drum project before starting a drumming session"""

import os
import subprocess
import time
import pyautogui
import sys


ASSETS_DIR = os.getenv("FL_ASSETS_DIR", "assets")  # Directory for reference images
FL_STUDIO_PATH = os.getenv("FL_STUDIO_PATH", "FL Studio 2024")
PROJECT_NAME = os.getenv("FL_PROJECT_NAME", "DRUMS.flp")
AUDIO_DEVICE = os.getenv("FL_AUDIO_DEVICE", "AIR 192 4")
WAIT_BETWEEN_TIME = int(
    os.getenv("WAIT_BETWEEN_TIME", "5")
)  # seconds to wait for FL Studio to launch


def launch_fl_studio():
    """Launch FL Studio using the configured path."""
    print("[INFO] Launching FL Studio...")
    subprocess.Popen(["open", "-a", FL_STUDIO_PATH])
    print("[INFO] FL Studio should be running now.")


def find_and_click(image_name, confidence=0.51, timeout=10):
    """
    Locate an image on the screen and click its center.
    Args:
        image_name (str): Filename of the image in the assets directory.
        confidence (float): Matching confidence (0-1).
        timeout (int): Seconds to keep searching before giving up.
    Raises:
        RuntimeError: If the image is not found within the timeout.
    """
    image_path = os.path.join(ASSETS_DIR, image_name)
    print(f"[INFO] Looking for {image_name}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        if location:
            pyautogui.moveTo(location)
            pyautogui.click()
            print(f"[INFO] Clicked {image_name} at {location}")
            return
        time.sleep(0.5)
    raise RuntimeError(f"Could not find {image_name} on screen.")


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


# TODO: NOT working property, Not focusing on the right window
def open_drum_project_screenshot():
    """
    Open the drum project in FL Studio using screenshot-based UI automation.
    """
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

    # Step 4: Click the project icon
    find_and_click("project_icon.png")
    time.sleep(1)

    # Step 5: Click the 'Open' button in the dialog
    find_and_click("dialog_open_button.png")
    time.sleep(1)

    # Step 6: Interact with EZD3 as needed, using more screenshots
    find_and_click("ezd3_file_button.png")
    time.sleep(1)
    find_and_click("open_recent.png")
    time.sleep(1)
    find_and_click("most_recent_save.png")
    time.sleep(1)
    find_and_click("bright_drumset.png")

    print("[INFO] Drum project opened using screenshots.")


def switch_audio_device():
    """Switch audio device to the one specified in the environment variable FL_AUDIO_DEVICE."""

    print(f"[INFO] Switching audio device to {AUDIO_DEVICE}...")

    # Move to and click on 265, 60 options
    pyautogui.moveTo(265, 60)
    pyautogui.click()
    time.sleep(1)

    # Move to and click on 295 120 audio settings
    pyautogui.moveTo(295, 120)
    pyautogui.click()
    time.sleep(1)

    # Move to and click on 640 160 Device
    pyautogui.moveTo(640, 160)
    pyautogui.click()
    time.sleep(1)

    # Move to and click on 640 230 Select
    pyautogui.moveTo(640, 230)
    pyautogui.click()
    time.sleep(1)

    # Move to and click on 640 230 Close
    pyautogui.moveTo(1078, 64)
    pyautogui.click()
    time.sleep(1)


def open_drum_session():
    launch_fl_studio()
    time.sleep(WAIT_BETWEEN_TIME)
    open_drum_project_pyautogui()
    time.sleep(WAIT_BETWEEN_TIME)
    switch_audio_device()


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

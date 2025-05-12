import os
import subprocess
import time

# Optional: Uncomment if you want to use pyautogui fallback
# import pyautogui

FL_STUDIO_PATH = os.getenv(
    "FL_STUDIO_PATH", r"C:\\Program Files\\Image-Line\\FL Studio 21\\FL64.exe"
)
PROJECT_NAME = os.getenv("FL_PROJECT_NAME", "DRUMS.flp")
WAIT_TIME = int(
    os.getenv("FL_WAIT_TIME", "10")
)  # seconds to wait for FL Studio to launch


def launch_fl_studio():
    """Launch FL Studio using the configured path."""
    print("[INFO] Launching FL Studio...")
    subprocess.Popen([FL_STUDIO_PATH])
    time.sleep(WAIT_TIME)
    print("[INFO] FL Studio should be running now.")


def open_project_with_cua():
    """
    Use OpenAI CuA to automate UI navigation:
    - Focus FL Studio window
    - Click 'File' (top left)
    - Select 'Open recent'
    - Click on PROJECT_NAME
    """
    # Pseudocode for OpenAI CuA API usage
    # Replace with actual API calls as per your setup
    print("[INFO] Using OpenAI CuA to automate UI...")
    # Example:
    # cua = OpenAICuA(api_key=os.getenv("OPENAI_API_KEY"))
    # cua.focus_window("FL Studio")
    # cua.click_menu("File")
    # cua.click_submenu("Open recent")
    # cua.click_menu_item(PROJECT_NAME)
    # If CuA is not available, fallback to pyautogui
    pass


def open_project_with_pyautogui():
    """
    Fallback: Use pyautogui to automate mouse/keyboard if CuA is not available.
    """
    print("[INFO] Using pyautogui as fallback...")
    # Uncomment and adjust the following if you want to use pyautogui
    # pyautogui.moveTo(30, 40, duration=0.5)  # Adjust coordinates as needed
    # pyautogui.click()
    # time.sleep(0.5)
    # pyautogui.press('down', presses=2, interval=0.2)
    # pyautogui.press('right')
    # for _ in range(10):
    #     if pyautogui.locateOnScreen(f"{PROJECT_NAME}.png", confidence=0.8):
    #         pyautogui.click(pyautogui.locateCenterOnScreen(f"{PROJECT_NAME}.png"))
    #         break
    #     pyautogui.press('down')
    # else:
    #     print("[ERROR] Project not found in recent files.")
    pass


def automate_fl_studio_open():
    launch_fl_studio()
    try:
        open_project_with_cua()
    except Exception as e:
        print(f"[WARN] CuA failed: {e}. Falling back to pyautogui.")
        open_project_with_pyautogui()


if __name__ == "__main__":
    automate_fl_studio_open()
